"""
Candidate Routes - Manage candidate information and history
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..dependencies import get_db
from ..models.candidate import Candidate
from ..models.application import Application
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
