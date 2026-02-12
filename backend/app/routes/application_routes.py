from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..models.candidate import Candidate
from ..models.job import Job
from ..models.company import Company
from ..models.application import Application
from ..services.embedding_service import get_embedding
from ..services.resume_parser_agent import parse_resume_pdf
from ..services.inference_engine import extract_skills_from_text
from ..services.audit_service import AuditService
from ..core.pipeline import run_pipeline, get_application_details

router = APIRouter(prefix="/apply", tags=["Application"])

@router.post("/{company_id}")
async def apply(
    company_id: int,
    name: str = Form(...),
    email: str = Form(...),
    mobile: str = Form(...),
    linkedin: str = Form(""),
    github: str = Form(""),
    experience: int = Form(...),
    resume_pdf: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Submit job application by uploading resume as PDF
    
    Endpoint: POST /apply/{company_id}
    - Automatically finds the job associated with the company
    """
    # Validate PDF file
    if not resume_pdf.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Verify company exists
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company ID {company_id} not found")
    
    # Find the job for this company
    job = db.query(Job).filter(Job.company_id == company_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail=f"No job found for Company ID {company_id}")
    
    # Check for duplicate email
    existing_candidate = db.query(Candidate).filter(Candidate.email == email).first()
    if existing_candidate:
        # Check if already applied to this job
        existing_application = db.query(Application).filter(
            Application.job_id == job.id,
            Application.candidate_id == existing_candidate.id
        ).first()
        
        if existing_application:
            raise HTTPException(
                status_code=400, 
                detail=f"You have already applied to this job. Application ID: {existing_application.id}"
            )
    
    # Read PDF content
    pdf_content = await resume_pdf.read()
    
    # Parse PDF to extract text
    parsed_resume = parse_resume_pdf(pdf_content)
    
    if not parsed_resume["success"]:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {parsed_resume.get('error')}")
    
    resume_text = parsed_resume["resume_text"]
    
    # Extract skills
    skills_data = extract_skills_from_text(resume_text)
    
    # Generate embedding
    emb = get_embedding(resume_text)

    # Create or update candidate record
    if existing_candidate:
        candidate = existing_candidate
    else:
        candidate = Candidate(
            name=name,
            email=email,
            mobile=mobile,
            linkedin=linkedin,
            github=github,
            experience=experience,
            resume_text=resume_text,
            resume_embedding=emb,
            skills_extracted=skills_data
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        
        # Log candidate registration
        AuditService.log_candidate_registration(db, candidate.id, email)

    # Run the hiring pipeline
    application = run_pipeline(db, job, candidate)

    return {
        "application_id": application.id,
        "candidate_id": candidate.id,
        "job_id": job.id,
        "company_id": company_id,
        "decision": application.decision,
        "composite_score": application.composite_score,
        "explanation": application.explanation,
        "message": "Application evaluated successfully",
        "pages_parsed": parsed_resume.get("page_count"),
        "skills_detected": skills_data["skill_count"]
    }


@router.get("/{application_id}")
def get_application(application_id: int, db: Session = Depends(get_db)):
    """Get complete application details with explanation"""
    details = get_application_details(db, application_id)
    
    if "error" in details:
        raise HTTPException(status_code=404, detail=details["error"])
    
    return details


@router.get("/{application_id}/history")
def get_application_history(application_id: int, db: Session = Depends(get_db)):
    """Get audit history for an application"""
    application = db.query(Application).filter(Application.id == application_id).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    history = AuditService.get_application_history(db, application_id)
    
    return {
        "application_id": application_id,
        "total_events": len(history),
        "history": history
    }


@router.get("/")
def list_applications(
    decision: str = None,
    fraud_flag: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List applications with optional filtering"""
    query = db.query(Application)
    
    if decision:
        query = query.filter(Application.decision == decision)
    
    if fraud_flag is not None:
        query = query.filter(Application.fraud_flag == fraud_flag)
    
    applications = query.order_by(Application.created_at.desc()).offset(skip).limit(limit).all()
    total = query.count()
    
    return {
        "total": total,
        "showing": len(applications),
        "skip": skip,
        "limit": limit,
        "applications": applications
    }
