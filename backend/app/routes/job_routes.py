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
from typing import List, Optional

router = APIRouter(prefix="/job", tags=["Job"])

@router.post("/create-with-company")
async def create_job_with_company(
    # Company details
    company_name: str = Form(...),
    company_description: str = Form(...),
    # Job details
    role: str = Form(...),
    location: str = Form(""),
    salary: str = Form(""),
    employment_type: str = Form("Full-time"),
    required_experience: int = Form(...),
    jd_pdf: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Create a new company and job posting in a single API call
    
    This merged endpoint handles both company registration and job posting.
    If a company with the same name exists, it will be reused.
    """
    # Validate PDF file
    if not jd_pdf.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Step 1: Create or get company
    existing_company = db.query(Company).filter(Company.name == company_name).first()
    
    if existing_company:
        company = existing_company
        company_status = "existing"
    else:
        company = Company(name=company_name, description=company_description)
        db.add(company)
        db.commit()
        db.refresh(company)
        company_status = "created"
    
    # Step 2: Read and parse PDF
    pdf_content = await jd_pdf.read()
    parsed_jd = parse_jd_pdf(pdf_content)
    
    if not parsed_jd["success"]:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {parsed_jd.get('error')}")
    
    jd_text = parsed_jd["jd_text"]
    
    # Step 3: Extract skills from JD
    skills_data = extract_skills_from_text(jd_text)
    
    # Step 4: Generate embedding
    emb = get_embedding(jd_text)

    # Step 5: Create job record
    job = Job(
        company_id=company.id,
        role=role,
        location=location if location else None,
        salary=salary if salary else None,
        employment_type=employment_type if employment_type else "Full-time",
        required_experience=required_experience,
        jd_text=jd_text,
        jd_embedding=emb,
        skills_extracted=skills_data
    )

    db.add(job)
    db.commit()
    db.refresh(job)
    
    # Step 6: Log job creation
    AuditService.log_job_creation(db, job.id, company.id, role)
    
    return {
        "company": {
            "id": company.id,
            "name": company.name,
            "description": company.description,
            "created_at": company.created_at.isoformat(),
            "status": company_status  # "created" or "existing"
        },
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
        "message": f"Company {company_status} and job created successfully",
        "pages_parsed": parsed_jd.get("page_count"),
        "skills_extracted": skills_data["all_skills"][:10],
        "technical_skills": skills_data["technical_skills"][:5],
        "soft_skills": skills_data["soft_skills"][:5]
    }

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


@router.get("/{company_id}/applications")
def get_company_applications(
    company_id: int,
    status_filter: str = None,
    db: Session = Depends(get_db)
):
    """Get all applications for all jobs of a specific company"""
    # Verify company exists
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get all jobs for this company
    jobs = db.query(Job).filter(Job.company_id == company_id).all()
    
    if not jobs:
        return {
            "company": {
                "id": company.id,
                "name": company.name
            },
            "total_applications": 0,
            "total_jobs": 0,
            "statistics": {
                "fast_track": 0,
                "selected": 0,
                "hire_pooled": 0,
                "rejected": 0,
                "review_required": 0
            },
            "applications": []
        }
    
    # Get all job IDs for this company
    job_ids = [job.id for job in jobs]
    
    # Query applications for all jobs of this company
    query = db.query(Application).filter(Application.job_id.in_(job_ids))
    
    if status_filter:
        query = query.filter(Application.decision == status_filter)
    
    applications = query.all()
    
    # Statistics across all jobs
    stats = {
        "fast_track": db.query(Application).filter(
            Application.job_id.in_(job_ids),
            Application.decision == "Fast-Track Selected"
        ).count(),
        "selected": db.query(Application).filter(
            Application.job_id.in_(job_ids),
            Application.decision == "Selected"
        ).count(),
        "hire_pooled": db.query(Application).filter(
            Application.job_id.in_(job_ids),
            Application.decision == "Hire-Pooled"
        ).count(),
        "rejected": db.query(Application).filter(
            Application.job_id.in_(job_ids),
            Application.decision == "Rejected"
        ).count(),
        "review_required": db.query(Application).filter(
            Application.job_id.in_(job_ids),
            Application.decision == "Review Required"
        ).count(),
    }
    
    return {
        "company": {
            "id": company.id,
            "name": company.name
        },
        "total_applications": len(applications),
        "total_jobs": len(jobs),
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
