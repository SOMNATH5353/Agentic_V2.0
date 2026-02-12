from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..dependencies import get_db
from ..models.job import Job
from ..models.application import Application
from ..models.company import Company
from ..services.embedding_service import get_embedding
from ..services.jd_parser_agent import parse_jd_pdf
from ..services.inference_engine import extract_skills_from_text
from ..services.audit_service import AuditService
from ..schemas.job_schema import JobListResponse
from typing import List

router = APIRouter(prefix="/job", tags=["Job"])

@router.post("/")
async def create_job(
    company_id: int = Form(...),
    role: str = Form(...),
    location: str = Form(""),
    salary: str = Form(""),
    employment_type: str = Form("Full-time"),
    required_experience: int = Form(...),
    jd_pdf: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Create a new job posting by uploading JD as PDF
    """
    # Validate PDF file
    if not jd_pdf.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Read PDF content
    pdf_content = await jd_pdf.read()
    
    # Parse PDF to extract text
    parsed_jd = parse_jd_pdf(pdf_content)
    
    if not parsed_jd["success"]:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {parsed_jd.get('error')}")
    
    jd_text = parsed_jd["jd_text"]
    
    # Extract skills from JD
    skills_data = extract_skills_from_text(jd_text)
    
    # Generate embedding
    emb = get_embedding(jd_text)

    # Create job record with embeddings and skills
    job = Job(
        company_id=company_id,
        role=role,
        location=location if location else None,
        salary=salary if salary else None,
        employment_type=employment_type if employment_type else "Full-time",
        required_experience=required_experience,
        jd_text=jd_text,
        jd_embedding=emb,
        skills_extracted=skills_data  # Store all skill data
    )

    db.add(job)
    db.commit()
    db.refresh(job)
    
    # Log job creation
    AuditService.log_job_creation(db, job.id, company_id, role)
    
    return {
        "job": {
            "id": job.id,
            "company_id": job.company_id,
            "role": job.role,
            "location": job.location,
            "salary": job.salary,
            "employment_type": job.employment_type,
            "required_experience": job.required_experience,
            "created_at": job.created_at.isoformat(),
            "jd_text_preview": jd_text[:200] + "..." if len(jd_text) > 200 else jd_text,
            "embedding_dimensions": len(emb) if emb else 0,
            "skills_stored": len(skills_data["all_skills"])
        },
        "message": "Job created and stored in database successfully",
        "pages_parsed": parsed_jd.get("page_count"),
        "skills_extracted": skills_data["all_skills"][:10],  # Top 10 skills for display
        "technical_skills": skills_data["technical_skills"][:5],
        "soft_skills": skills_data["soft_skills"][:5]
    }


@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Get detailed job information by ID
    Returns full job details including JD text for candidate review
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get application statistics
    application_count = db.query(Application).filter(Application.job_id == job_id).count()
    
    return {
        "id": job.id,
        "company_id": job.company_id,
        "company_name": job.company.name if job.company else "Unknown",
        "company_description": job.company.description if job.company else "",
        "role": job.role,
        "location": job.location,
        "salary": job.salary,
        "employment_type": job.employment_type,
        "required_experience": job.required_experience,
        "jd_text": job.jd_text,
        "created_at": job.created_at.isoformat(),
        "application_count": application_count,
        "skills_required": job.skills_extracted.get("all_skills", []) if job.skills_extracted else [],
        "technical_skills": job.skills_extracted.get("technical_skills", []) if job.skills_extracted else [],
        "soft_skills": job.skills_extracted.get("soft_skills", []) if job.skills_extracted else []
    }


@router.get("/{job_id}/applications")
def get_job_applications(
    job_id: int,
    status_filter: str = None,
    db: Session = Depends(get_db)
):
    """Get all applications for a specific job"""
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    query = db.query(Application).filter(Application.job_id == job_id)
    
    if status_filter:
        query = query.filter(Application.decision == status_filter)
    
    applications = query.all()
    
    # Statistics
    stats = {
        "fast_track": db.query(Application).filter(
            Application.job_id == job_id,
            Application.decision == "Fast-Track Selected"
        ).count(),
        "selected": db.query(Application).filter(
            Application.job_id == job_id,
            Application.decision == "Selected"
        ).count(),
        "hire_pooled": db.query(Application).filter(
            Application.job_id == job_id,
            Application.decision == "Hire-Pooled"
        ).count(),
        "rejected": db.query(Application).filter(
            Application.job_id == job_id,
            Application.decision == "Rejected"
        ).count(),
        "review_required": db.query(Application).filter(
            Application.job_id == job_id,
            Application.decision == "Review Required"
        ).count(),
    }
    
    return {
        "job": {
            "id": job.id,
            "role": job.role,
            "company_id": job.company_id
        },
        "total_applications": len(applications),
        "statistics": stats,
        "applications": applications
    }


@router.get("/", response_model=dict)
def list_jobs(
    company_id: int = None,
    location: str = None,
    employment_type: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all available jobs with filtering options
    Returns job listings with company information for candidate browsing
    """
    query = db.query(Job).join(Company)
    
    if company_id:
        query = query.filter(Job.company_id == company_id)
    
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    
    if employment_type:
        query = query.filter(Job.employment_type == employment_type)
    
    # Order by most recent first
    query = query.order_by(Job.created_at.desc())
    
    total = query.count()
    jobs = query.offset(skip).limit(limit).all()
    
    # Enrich job data with company info and application counts
    jobs_data = []
    for job in jobs:
        application_count = db.query(Application).filter(Application.job_id == job.id).count()
        
        jobs_data.append({
            "id": job.id,
            "role": job.role,
            "company_id": job.company_id,
            "company_name": job.company.name if job.company else "Unknown",
            "location": job.location,
            "salary": job.salary,
            "employment_type": job.employment_type,
            "required_experience": job.required_experience,
            "created_at": job.created_at.isoformat(),
            "application_count": application_count,
            "skills_preview": job.skills_extracted.get("all_skills", [])[:5] if job.skills_extracted else []
        })
    
    return {
        "total": total,
        "showing": len(jobs_data),
        "skip": skip,
        "limit": limit,
        "jobs": jobs_data
    }
