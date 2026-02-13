from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from ..dependencies import get_db
from ..models.application import Application
from ..models.candidate import Candidate
from ..models.job import Job
from ..models.company import Company
from ..services.pdf_report_service import master_report_generator
from typing import List, Dict, Any
from io import BytesIO

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/application/{application_id}/xai")
def get_xai_explanation(application_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive XAI (Explainable AI) explanation for an application
    
    Returns transparent, detailed explanation of why a decision was made
    """
    application = db.query(Application).filter(Application.id == application_id).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Extract XAI explanation from stored explanation
    full_explanation = application.explanation or {}
    xai_explanation = full_explanation.get("xai_explanation", {})
    
    if not xai_explanation:
        raise HTTPException(status_code=404, detail="XAI explanation not available for this application")
    
    # Get candidate and job info for context
    candidate = db.query(Candidate).filter(Candidate.id == application.candidate_id).first()
    job = db.query(Job).filter(Job.id == application.job_id).first()
    
    return {
        "application_id": application_id,
        "candidate": {
            "name": candidate.name,
            "experience": candidate.experience
        },
        "job": {
            "role": job.role,
            "required_experience": job.required_experience
        },
        "xai_explanation": xai_explanation
    }


@router.get("/application/{application_id}/skill-gap")
def get_skill_gap_analysis(application_id: int, db: Session = Depends(get_db)):
    """
    Get detailed skill gap analysis for an application
    
    Returns:
        - Skills matched vs missing
        - Gap severity
        - Learning roadmap
        - Recommendations
    """
    application = db.query(Application).filter(Application.id == application_id).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    full_explanation = application.explanation or {}
    skill_gap = full_explanation.get("skill_gap_analysis", {})
    
    if not skill_gap:
        raise HTTPException(status_code=404, detail="Skill gap analysis not available")
    
    # Get candidate and job info
    candidate = db.query(Candidate).filter(Candidate.id == application.candidate_id).first()
    job = db.query(Job).filter(Job.id == application.job_id).first()
    
    return {
        "application_id": application_id,
        "candidate": {
            "name": candidate.name,
            "email": candidate.email
        },
        "job": {
            "role": job.role
        },
        "skill_gap_analysis": skill_gap
    }


@router.get("/application/{application_id}/skill-graph")
def get_skill_evidence_graph(application_id: int, db: Session = Depends(get_db)):
    """
    Get skill evidence graph data for visualization
    
    Returns graph data structure ready for frontend visualization
    (Compatible with D3.js, Chart.js, or other graph libraries)
    """
    application = db.query(Application).filter(Application.id == application_id).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    full_explanation = application.explanation or {}
    skill_graph = full_explanation.get("skill_evidence_graph", {})
    
    if not skill_graph:
        raise HTTPException(status_code=404, detail="Skill evidence graph not available")
    
    return {
        "application_id": application_id,
        "skill_evidence_graph": skill_graph
    }


@router.get("/job/{job_id}/rankings")
def get_job_application_rankings(
    job_id: int,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get ranked list of all applications for a job
    
    Returns applications sorted by rank (best to worst)
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get all applications ordered by rank
    applications = db.query(Application).filter(
        Application.job_id == job_id
    ).order_by(Application.rank.asc()).limit(limit).all()
    
    # Enrich with candidate info
    rankings = []
    for app in applications:
        candidate = db.query(Candidate).filter(Candidate.id == app.candidate_id).first()
        
        rankings.append({
            "rank": app.rank,
            "application_id": app.id,
            "candidate": {
                "id": candidate.id,
                "name": candidate.name,
                "email": candidate.email,
                "experience": candidate.experience
            },
            "scores": {
                "composite_score": app.composite_score,
                "rfs": app.rfs,
                "dcs": app.dcs,
                "elc": app.elc
            },
            "decision": app.decision,
            "fraud_flag": app.fraud_flag,
            "created_at": app.created_at.isoformat()
        })
    
    return {
        "job": {
            "id": job.id,
            "role": job.role,
            "company_id": job.company_id
        },
        "total_applications": len(rankings),
        "rankings": rankings
    }


@router.get("/job/{job_id}/top-candidates")
def get_top_candidates(
    job_id: int,
    top_n: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get top N candidates for a job based on ranking
    
    Useful for recruiter dashboard to quickly see best matches
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get top N non-fraud applications
    top_apps = db.query(Application).filter(
        Application.job_id == job_id,
        Application.fraud_flag == False
    ).order_by(Application.rank.asc()).limit(top_n).all()
    
    top_candidates = []
    for app in top_apps:
        candidate = db.query(Candidate).filter(Candidate.id == app.candidate_id).first()
        
        # Get skill match summary
        skill_match = app.skill_match or {}
        
        top_candidates.append({
            "rank": app.rank,
            "application_id": app.id,
            "candidate": {
                "id": candidate.id,
                "name": candidate.name,
                "email": candidate.email,
                "mobile": candidate.mobile,
                "experience": candidate.experience,
                "linkedin": candidate.linkedin,
                "github": candidate.github
            },
            "scores": {
                "composite_score": app.composite_score,
                "match_percentage": f"{app.composite_score * 100:.1f}%"
            },
            "skill_match_summary": {
                "matched_skills_count": len(skill_match.get("matched_skills", [])),
                "missing_skills_count": len(skill_match.get("missing_skills", [])),
                "match_score": skill_match.get("match_score", 0)
            },
            "decision": app.decision,
            "created_at": app.created_at.isoformat()
        })
    
    return {
        "job": {
            "id": job.id,
            "role": job.role,
            "company_id": job.company_id
        },
        "top_n": top_n,
        "top_candidates": top_candidates
    }


@router.get("/job/{job_id}/statistics")
def get_job_statistics(job_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive statistics for a job's applications
    
    Includes:
        - Total applications
        - Decision breakdown
        - Average scores
        - Ranking distribution
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    all_apps = db.query(Application).filter(Application.job_id == job_id).all()
    
    if not all_apps:
        return {
            "job_id": job_id,
            "message": "No applications yet"
        }
    
    # Calculate statistics
    total = len(all_apps)
    
    # Decision counts
    decisions = {}
    for app in all_apps:
        decision = app.decision or "Unknown"
        decisions[decision] = decisions.get(decision, 0) + 1
    
    # Average scores
    avg_composite = sum(app.composite_score or 0 for app in all_apps) / total
    avg_rfs = sum(app.rfs or 0 for app in all_apps) / total
    avg_dcs = sum(app.dcs or 0 for app in all_apps) / total
    avg_elc = sum(app.elc or 0 for app in all_apps) / total
    
    # Fraud statistics
    fraud_count = sum(1 for app in all_apps if app.fraud_flag)
    
    # Top candidate
    top_candidate_app = db.query(Application).filter(
        Application.job_id == job_id,
        Application.fraud_flag == False
    ).order_by(Application.rank.asc()).first()
    
    top_candidate_info = None
    if top_candidate_app:
        top_candidate = db.query(Candidate).filter(
            Candidate.id == top_candidate_app.candidate_id
        ).first()
        top_candidate_info = {
            "name": top_candidate.name,
            "rank": top_candidate_app.rank,
            "score": top_candidate_app.composite_score,
            "decision": top_candidate_app.decision
        }
    
    return {
        "job": {
            "id": job.id,
            "role": job.role,
            "company_id": job.company_id
        },
        "total_applications": total,
        "decision_breakdown": decisions,
        "average_scores": {
            "composite": round(avg_composite, 4),
            "rfs": round(avg_rfs, 4),
            "dcs": round(avg_dcs, 4),
            "elc": round(avg_elc, 4)
        },
        "fraud_statistics": {
            "total_fraud": fraud_count,
            "fraud_percentage": round(fraud_count / total * 100, 2)
        },
        "top_candidate": top_candidate_info
    }


@router.get("/candidate/{candidate_id}/applications")
def get_candidate_applications(candidate_id: int, db: Session = Depends(get_db)):
    """
    Get all applications submitted by a candidate
    
    Useful for candidate portal to track their applications
    """
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    applications = db.query(Application).filter(
        Application.candidate_id == candidate_id
    ).order_by(desc(Application.created_at)).all()
    
    applications_data = []
    for app in applications:
        job = db.query(Job).filter(Job.id == app.job_id).first()
        company = db.query(Company).filter(Company.id == job.company_id).first() if job else None
        
        applications_data.append({
            "application_id": app.id,
            "job": {
                "id": job.id,
                "role": job.role,
                "company_name": company.name if company else "Unknown"
            },
            "rank": app.rank,
            "scores": {
                "composite_score": app.composite_score,
                "percentage": f"{app.composite_score * 100:.1f}%"
            },
            "decision": app.decision,
            "status": app.status,
            "applied_at": app.created_at.isoformat()
        })
    
    return {
        "candidate": {
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email
        },
        "total_applications": len(applications_data),
        "applications": applications_data
    }


@router.get("/candidates/dashboard")
def get_candidates_dashboard(
    skip: int = 0,
    limit: int = 100,
    tier_filter: str = None,
    status_filter: str = None,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive candidates dashboard with all details
    
    Returns: total candidates, statistics, and detailed candidate information
    including tier classification, applications, scores, and decisions
    
    Query Parameters:
    - tier_filter: Filter by tier (Excellent/Good/Average/Poor)
    - status_filter: Filter by status (Selected/Rejected/Pending)
    - skip: Pagination offset
    - limit: Maximum results (default 100)
    """
    
    def get_tier(score: float) -> str:
        """Classify candidate into tier based on composite score"""
        if score >= 0.85:
            return "Excellent"
        elif score >= 0.70:
            return "Good"
        elif score >= 0.50:
            return "Average"
        else:
            return "Poor"
    
    def get_status(decision: str) -> str:
        """Convert decision to status"""
        if decision in ["Fast-Track Selected", "Selected"]:
            return "Selected"
        elif decision == "Rejected":
            return "Rejected"
        else:
            return "Pending"
    
    # Get all candidates with their applications
    candidates = db.query(Candidate).all()
    
    # Build comprehensive candidate data
    candidates_data = []
    
    for candidate in candidates:
        # Get all applications for this candidate
        applications = db.query(Application).filter(
            Application.candidate_id == candidate.id
        ).all()
        
        if not applications:
            continue  # Skip candidates with no applications
        
        # Get best application (highest score)
        best_app = max(applications, key=lambda x: x.composite_score)
        
        # Get job and company details
        job = db.query(Job).filter(Job.id == best_app.job_id).first()
        company = db.query(Company).filter(Company.id == job.company_id).first() if job else None
        
        # Calculate tier and status
        tier = get_tier(best_app.composite_score)
        status = get_status(best_app.decision)
        
        # Build candidate entry
        candidate_entry = {
            "candidate_id": candidate.id,
            "candidate_name": candidate.name,
            "email": candidate.email,
            "mobile": candidate.mobile,
            "experience": candidate.experience,
            "total_applications": len(applications),
            "best_application": {
                "application_id": best_app.id,
                "job_role": job.role if job else "Unknown",
                "company_name": company.name if company else "Unknown",
                "company_id": company.id if company else None,
                "applied_date": best_app.created_at.isoformat()
            },
            "scores": {
                "composite_score": round(best_app.composite_score, 2),
                "percentage": f"{best_app.composite_score * 100:.1f}%",
                "rfs": round(best_app.rfs, 2),
                "dcs": round(best_app.dcs, 2),
                "elc": round(best_app.elc, 2)
            },
            "decision": best_app.decision,
            "status": status,
            "tier": tier,
            "rank": best_app.rank,
            "fraud_flag": best_app.fraud_flag
        }
        
        # Apply filters
        if tier_filter and tier != tier_filter:
            continue
        if status_filter and status != status_filter:
            continue
        
        candidates_data.append(candidate_entry)
    
    # Sort by composite score (highest first)
    candidates_data.sort(key=lambda x: x["scores"]["composite_score"], reverse=True)
    
    # Calculate statistics
    total_candidates = len(candidates_data)
    
    stats = {
        "total_candidates": total_candidates,
        "by_status": {
            "selected": len([c for c in candidates_data if c["status"] == "Selected"]),
            "rejected": len([c for c in candidates_data if c["status"] == "Rejected"]),
            "pending": len([c for c in candidates_data if c["status"] == "Pending"])
        },
        "by_tier": {
            "excellent": len([c for c in candidates_data if c["tier"] == "Excellent"]),
            "good": len([c for c in candidates_data if c["tier"] == "Good"]),
            "average": len([c for c in candidates_data if c["tier"] == "Average"]),
            "poor": len([c for c in candidates_data if c["tier"] == "Poor"])
        },
        "by_decision": {
            "fast_track": len([c for c in candidates_data if c["decision"] == "Fast-Track Selected"]),
            "selected": len([c for c in candidates_data if c["decision"] == "Selected"]),
            "hire_pooled": len([c for c in candidates_data if c["decision"] == "Hire-Pooled"]),
            "rejected": len([c for c in candidates_data if c["decision"] == "Rejected"]),
            "review_required": len([c for c in candidates_data if c["decision"] == "Review Required"])
        },
        "average_score": round(sum(c["scores"]["composite_score"] for c in candidates_data) / total_candidates, 2) if total_candidates > 0 else 0
    }
    
    # Apply pagination
    paginated_data = candidates_data[skip:skip + limit]
    
    return {
        "statistics": stats,
        "filters_applied": {
            "tier_filter": tier_filter,
            "status_filter": status_filter
        },
        "pagination": {
            "total": total_candidates,
            "showing": len(paginated_data),
            "skip": skip,
            "limit": limit
        },
        "candidates": paginated_data
    }


@router.get("/master-report/pdf")
def generate_master_pdf_report(
    limit: int = 50,
    skip: int = 0,
    db: Session = Depends(get_db)
):
    """
    🆕 MASTER PDF REPORT - Generate comprehensive PDF report for all candidates
    
    This endpoint generates a complete PDF report containing:
    - Executive summary with statistics
    - All candidate profiles
    - Application rankings
    - XAI explanations
    - Skill gap analysis
    - Skill match details
    - Score visualizations
    - Fraud detection results
    
    Query Parameters:
    - limit: Maximum number of candidates to include (default: 50, max: 100)
    - skip: Number of candidates to skip (default: 0)
    
    Returns:
    - PDF file (application/pdf)
    
    Example:
    GET /analytics/master-report/pdf?limit=20
    """
    # Limit the maximum
    if limit > 100:
        limit = 100
    
    # Get all candidates with pagination
    all_candidates = db.query(Candidate).order_by(Candidate.created_at.desc()).offset(skip).limit(limit).all()
    
    if not all_candidates:
        raise HTTPException(status_code=404, detail="No candidates found")
    
    # Build comprehensive data for each candidate
    candidates_master_data = []
    
    for candidate in all_candidates:
        # Get all applications for this candidate
        applications = db.query(Application).filter(
            Application.candidate_id == candidate.id
        ).order_by(Application.composite_score.desc()).all()
        
        # Build application details with analytics
        application_details = []
        for app in applications:
            job = db.query(Job).filter(Job.id == app.job_id).first()
            company = None
            if job:
                company = db.query(Company).filter(Company.id == job.company_id).first()
            
            # Extract XAI explanation
            full_explanation = app.explanation or {}
            xai_explanation = full_explanation.get("xai_explanation", {})
            skill_gap = full_explanation.get("skill_gap_analysis", {})
            skill_graph = full_explanation.get("skill_evidence_graph", {})
            
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
                    "company_name": company.name if company else None,
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
                },
                
                # XAI Explanation
                "xai_explanation": xai_explanation,
                
                # Skill Gap Analysis
                "skill_gap_analysis": skill_gap,
                
                # Skill Evidence Graph
                "skill_evidence_graph": skill_graph
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
                "skills": candidate.skills_extracted.get("technical_skills", []) if candidate.skills_extracted else [],
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
    
    # Generate PDF
    try:
        pdf_buffer = master_report_generator.generate_master_report(candidates_master_data)
        
        # Return as streaming response
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=master_candidate_report_{skip}_{limit}.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
