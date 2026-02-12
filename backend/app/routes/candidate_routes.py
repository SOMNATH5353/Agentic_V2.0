"""
Candidate Routes - Manage candidate information and history
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..dependencies import get_db
from ..models.candidate import Candidate
from ..models.application import Application
from ..models.job import Job
from ..models.company import Company
from ..services.audit_service import AuditService

router = APIRouter(prefix="/candidate", tags=["Candidate"])


@router.get("/{candidate_id}")
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """Get candidate details by ID"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return candidate


@router.get("/{candidate_id}/applications")
def get_candidate_applications(candidate_id: int, db: Session = Depends(get_db)):
    """Get all applications submitted by a candidate"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    applications = db.query(Application).filter(
        Application.candidate_id == candidate_id
    ).all()
    
    return {
        "candidate": {
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email
        },
        "total_applications": len(applications),
        "applications": applications
    }


@router.get("/{candidate_id}/history")
def get_candidate_history(candidate_id: int, db: Session = Depends(get_db)):
    """Get complete audit history for a candidate"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    history = AuditService.get_candidate_history(db, candidate_id)
    
    return {
        "candidate_id": candidate_id,
        "total_events": len(history),
        "history": history
    }


@router.get("/search/by-email")
def search_candidate_by_email(email: str, db: Session = Depends(get_db)):
    """Search for candidate by email"""
    candidate = db.query(Candidate).filter(Candidate.email == email).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return candidate


@router.get("/")
def list_candidates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all candidates with pagination"""
    candidates = db.query(Candidate).offset(skip).limit(limit).all()
    total = db.query(Candidate).count()
    
    return {
        "total": total,
        "showing": len(candidates),
        "skip": skip,
        "limit": limit,
        "candidates": candidates
    }


@router.get("/{candidate_id}/master")
def get_candidate_master_details(candidate_id: int, db: Session = Depends(get_db)):
    """
    Master Endpoint - Get complete candidate profile with all details:
    - Personal information (name, email, mobile, linkedin, github, experience)
    - Skills extracted from resume
    - All applications with detailed information
    - Each application includes:
        - Job details (role, location, salary, company)
        - All scores (RFS, DCS, ELC, Composite Score)
        - Ranking among applicants
        - Decision (Selected/Rejected/Pending)
        - Decision reason and explanation
        - Fraud detection details
        - Skill match analysis
        - Application status
    """
    # Get candidate details
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Get all applications with job and company details
    applications = db.query(Application).filter(
        Application.candidate_id == candidate_id
    ).all()
    
    # Build comprehensive application details
    application_details = []
    for app in applications:
        job = db.query(Job).filter(Job.id == app.job_id).first()
        company = None
        if job:
            company = db.query(Company).filter(Company.id == job.company_id).first()
        
        application_info = {
            "application_id": app.id,
            "applied_at": app.created_at.isoformat() if app.created_at else None,
            "status": app.status,
            
            # Job Details
            "job_details": {
                "job_id": job.id if job else None,
                "role": job.role if job else None,
                "location": job.location if job else None,
                "salary": job.salary if job else None,
                "employment_type": job.employment_type if job else None,
                "required_experience": job.required_experience if job else None,
                "job_description": job.jd_text if job else None,
                "required_skills": job.skills_extracted if job else None,
            } if job else None,
            
            # Company Details
            "company_details": {
                "company_id": company.id if company else None,
                "company_name": company.name if company else None,
                "company_description": company.description if company else None,
            } if company else None,
            
            # Scores
            "scores": {
                "role_fit_score": app.rfs,
                "domain_competency_score": app.dcs,
                "experience_level_compatibility": app.elc,
                "composite_score": app.composite_score,
                "rank": app.rank,
                "rank_description": f"Ranked #{app.rank}" if app.rank else "Not ranked yet"
            },
            
            # Decision
            "decision": {
                "status": app.decision if app.decision else "Pending",
                "reason": app.decision_reason,
                "detailed_explanation": app.explanation
            },
            
            # Fraud Detection
            "fraud_detection": {
                "fraud_flag": app.fraud_flag,
                "similarity_index": app.similarity_index,
                "fraud_details": app.fraud_details
            },
            
            # Skill Analysis
            "skill_analysis": {
                "skill_match": app.skill_match,
                "experience_details": app.experience_details
            }
        }
        
        application_details.append(application_info)
    
    # Calculate summary statistics
    total_applications = len(applications)
    selected_count = sum(1 for app in applications if app.decision == "Selected")
    rejected_count = sum(1 for app in applications if app.decision == "Rejected")
    pending_count = sum(1 for app in applications if not app.decision or app.decision == "Pending")
    
    avg_composite_score = None
    if applications:
        scores = [app.composite_score for app in applications if app.composite_score is not None]
        if scores:
            avg_composite_score = sum(scores) / len(scores)
    
    best_application = None
    if applications:
        scored_apps = [app for app in applications if app.composite_score is not None]
        if scored_apps:
            best_app = max(scored_apps, key=lambda x: x.composite_score)
            best_job = db.query(Job).filter(Job.id == best_app.job_id).first()
            best_application = {
                "application_id": best_app.id,
                "job_role": best_job.role if best_job else None,
                "composite_score": best_app.composite_score,
                "decision": best_app.decision,
                "rank": best_app.rank
            }
    
    # Build master response
    master_data = {
        "candidate_profile": {
            "candidate_id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "mobile": candidate.mobile,
            "linkedin": candidate.linkedin,
            "github": candidate.github,
            "years_of_experience": candidate.experience,
            "skills": candidate.skills_extracted,
            "resume_text": candidate.resume_text,
            "profile_created_at": candidate.created_at.isoformat() if candidate.created_at else None
        },
        
        "application_summary": {
            "total_applications": total_applications,
            "selected": selected_count,
            "rejected": rejected_count,
            "pending": pending_count,
            "average_composite_score": round(avg_composite_score, 2) if avg_composite_score else None,
            "best_application": best_application
        },
        
        "applications": application_details
    }
    
    return master_data


@router.get("/master/all")
def get_all_candidates_master_details(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Master Endpoint - Get complete details for ALL candidates with pagination.
    Returns comprehensive information for all candidates including:
    - Personal information for each candidate
    - All their applications with scores, decisions, and analysis
    - Summary statistics per candidate
    
    Query Parameters:
    - skip: Number of candidates to skip (default: 0)
    - limit: Maximum number of candidates to return (default: 100, max: 500)
    """
    # Limit the maximum number of candidates that can be fetched at once
    if limit > 500:
        limit = 500
    
    # Get all candidates with pagination
    all_candidates = db.query(Candidate).offset(skip).limit(limit).all()
    total_candidates = db.query(Candidate).count()
    
    if not all_candidates:
        return {
            "total_candidates": total_candidates,
            "showing": 0,
            "skip": skip,
            "limit": limit,
            "candidates": []
        }
    
    # Build comprehensive data for each candidate
    candidates_master_data = []
    
    for candidate in all_candidates:
        # Get all applications for this candidate
        applications = db.query(Application).filter(
            Application.candidate_id == candidate.id
        ).all()
        
        # Build application details
        application_details = []
        for app in applications:
            job = db.query(Job).filter(Job.id == app.job_id).first()
            company = None
            if job:
                company = db.query(Company).filter(Company.id == job.company_id).first()
            
            application_info = {
                "application_id": app.id,
                "applied_at": app.created_at.isoformat() if app.created_at else None,
                "status": app.status,
                
                # Job Details
                "job_details": {
                    "job_id": job.id if job else None,
                    "role": job.role if job else None,
                    "location": job.location if job else None,
                    "salary": job.salary if job else None,
                    "employment_type": job.employment_type if job else None,
                    "required_experience": job.required_experience if job else None,
                    "job_description": job.jd_text if job else None,
                    "required_skills": job.skills_extracted if job else None,
                } if job else None,
                
                # Company Details
                "company_details": {
                    "company_id": company.id if company else None,
                    "company_name": company.name if company else None,
                    "company_description": company.description if company else None,
                } if company else None,
                
                # Scores
                "scores": {
                    "role_fit_score": app.rfs,
                    "domain_competency_score": app.dcs,
                    "experience_level_compatibility": app.elc,
                    "composite_score": app.composite_score,
                    "rank": app.rank,
                    "rank_description": f"Ranked #{app.rank}" if app.rank else "Not ranked yet"
                },
                
                # Decision
                "decision": {
                    "status": app.decision if app.decision else "Pending",
                    "reason": app.decision_reason,
                    "detailed_explanation": app.explanation
                },
                
                # Fraud Detection
                "fraud_detection": {
                    "fraud_flag": app.fraud_flag,
                    "similarity_index": app.similarity_index,
                    "fraud_details": app.fraud_details
                },
                
                # Skill Analysis
                "skill_analysis": {
                    "skill_match": app.skill_match,
                    "experience_details": app.experience_details
                }
            }
            
            application_details.append(application_info)
        
        # Calculate summary statistics for this candidate
        total_applications = len(applications)
        selected_count = sum(1 for app in applications if app.decision == "Selected")
        rejected_count = sum(1 for app in applications if app.decision == "Rejected")
        pending_count = sum(1 for app in applications if not app.decision or app.decision == "Pending")
        
        avg_composite_score = None
        if applications:
            scores = [app.composite_score for app in applications if app.composite_score is not None]
            if scores:
                avg_composite_score = sum(scores) / len(scores)
        
        best_application = None
        if applications:
            scored_apps = [app for app in applications if app.composite_score is not None]
            if scored_apps:
                best_app = max(scored_apps, key=lambda x: x.composite_score)
                best_job = db.query(Job).filter(Job.id == best_app.job_id).first()
                best_application = {
                    "application_id": best_app.id,
                    "job_role": best_job.role if best_job else None,
                    "composite_score": best_app.composite_score,
                    "decision": best_app.decision,
                    "rank": best_app.rank
                }
        
        # Build master data for this candidate
        candidate_master = {
            "candidate_profile": {
                "candidate_id": candidate.id,
                "name": candidate.name,
                "email": candidate.email,
                "mobile": candidate.mobile,
                "linkedin": candidate.linkedin,
                "github": candidate.github,
                "years_of_experience": candidate.experience,
                "skills": candidate.skills_extracted,
                "resume_text": candidate.resume_text,
                "profile_created_at": candidate.created_at.isoformat() if candidate.created_at else None
            },
            
            "application_summary": {
                "total_applications": total_applications,
                "selected": selected_count,
                "rejected": rejected_count,
                "pending": pending_count,
                "average_composite_score": round(avg_composite_score, 2) if avg_composite_score else None,
                "best_application": best_application
            },
            
            "applications": application_details
        }
        
        candidates_master_data.append(candidate_master)
    
    # Calculate global statistics
    total_applications_all = sum(c["application_summary"]["total_applications"] for c in candidates_master_data)
    total_selected_all = sum(c["application_summary"]["selected"] for c in candidates_master_data)
    total_rejected_all = sum(c["application_summary"]["rejected"] for c in candidates_master_data)
    total_pending_all = sum(c["application_summary"]["pending"] for c in candidates_master_data)
    
    return {
        "total_candidates": total_candidates,
        "showing": len(candidates_master_data),
        "skip": skip,
        "limit": limit,
        "global_statistics": {
            "total_applications": total_applications_all,
            "total_selected": total_selected_all,
            "total_rejected": total_rejected_all,
            "total_pending": total_pending_all
        },
        "candidates": candidates_master_data
    }
