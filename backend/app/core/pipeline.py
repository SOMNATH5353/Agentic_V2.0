"""
Enhanced AI Hiring Pipeline
Integrates all evaluation components for comprehensive candidate assessment
"""
from ..services.scoring_engine import compute_all_scores
from ..services.fraud_detection import comprehensive_fraud_analysis
from ..services.decision_service import make_decision
from ..services.explanation_agent import explain_decision
from ..services.xai_explainability import generate_xai_explanation
from ..services.skill_gap_analysis import analyze_skill_gap, generate_skill_evidence_graph
from ..services.audit_service import log_evaluation, log_fraud
from ..models.application import Application
from ..models.candidate import Candidate
from sqlalchemy import desc
import json


def run_pipeline(db, job, candidate):
    """
    Execute complete hiring evaluation pipeline
    
    Steps:
    1. Compute all scores (RFS, DCS, ELC, Composite)
    2. Perform comprehensive fraud detection
    3. Make hiring decision
    4. Generate explanation
    5. Log audit trail
    6. Store application
    
    Args:
        db: Database session
        job: Job model instance
        candidate: Candidate model instance
        
    Returns:
        Application record with complete evaluation
    """
    
    # Step 1: Compute All Scores
    print(f"[Pipeline] Evaluating candidate {candidate.id} for job {job.id}")
    score_results = compute_all_scores(job, candidate)
    
    rfs = score_results["rfs"]
    dcs = score_results["dcs"]
    elc = score_results["elc"]
    composite = score_results["composite_score"]
    skill_match = score_results["skill_match"]
    exp_details = score_results["experience_details"]
    breakdown = score_results["breakdown"]
    
    print(f"[Pipeline] Scores - RFS: {rfs:.2f}, DCS: {dcs:.2f}, ELC: {elc:.2f}, Composite: {composite:.2f}")
    
    # Step 2: Comprehensive Fraud Detection
    existing = db.query(Candidate).filter(Candidate.id != candidate.id).all()
    
    fraud_analysis = comprehensive_fraud_analysis(
        candidate.resume_embedding,
        candidate.resume_text,
        candidate.email,
        existing
    )
    
    fraud_flag = fraud_analysis["fraud_flag"]
    sim_index = fraud_analysis["similarity_index"]
    
    print(f"[Pipeline] Fraud Check - Flag: {fraud_flag}, Similarity: {sim_index:.2f}")
    
    # Log fraud if detected
    if fraud_flag:
        log_fraud(db, candidate.id, fraud_analysis)
    
    # Step 3: Make Decision
    decision, decision_reason = make_decision(
        rfs, dcs, elc, composite, 
        fraud_flag, sim_index,
        fraud_analysis, skill_match, exp_details
    )
    
    print(f"[Pipeline] Decision: {decision} - {decision_reason}")
    
    # Step 4: Generate Explanation
    explanation = explain_decision(
        decision,
        {
            "rfs": rfs,
            "dcs": dcs,
            "elc": elc,
            "composite_score": composite
        },
        skill_match,
        exp_details,
        fraud_analysis
    )
    
    # Step 4.5: Generate Skill Gap Analysis (now considers required vs nice-to-have!)
    skill_gap = analyze_skill_gap(
        skill_match.get("matched_skills", []),
        skill_match.get("missing_skills", []),
        skill_match.get("candidate_extras", []),
        job.jd_text,
        candidate.resume_text,
        skill_match  # Pass full skill_match details for enhanced analysis
    )
    
    # Step 4.6: Generate XAI Explainability
    xai_explanation = generate_xai_explanation(
        decision,
        {
            "rfs": rfs,
            "dcs": dcs,
            "elc": elc,
            "composite_score": composite,
            "breakdown": breakdown
        },
        skill_match,
        exp_details,
        fraud_analysis,
        skill_gap
    )
    
    # Step 4.7: Generate Skill Evidence Graph
    skill_graph = generate_skill_evidence_graph(
        skill_match.get("matched_skills", []),
        skill_match.get("missing_skills", []),
        skill_match.get("candidate_extras", []),
        score_results.get("jd_skills", {}).get("technical_skills", []),
        score_results.get("resume_skills", {}).get("technical_skills", [])
    )
    
    # Step 5: Create Application Record
    application = Application(
        job_id=job.id,
        candidate_id=candidate.id,
        rfs=rfs,
        dcs=dcs,
        elc=elc,
        composite_score=composite,
        similarity_index=sim_index,
        fraud_flag=fraud_flag,
        fraud_details=fraud_analysis,
        decision=decision,
        decision_reason=decision_reason,
        explanation={
            "basic_explanation": explanation,
            "xai_explanation": xai_explanation,
            "skill_gap_analysis": skill_gap,
            "skill_evidence_graph": skill_graph
        },
        skill_match=skill_match,
        experience_details=exp_details,
        status="evaluated"
    )
    
    db.add(application)
    db.commit()
    db.refresh(application)
    
    print(f"[Pipeline] Application {application.id} created")
    
    # Step 6: Update Rankings for this job
    update_application_rankings(db, job.id)
    print(f"[Pipeline] Rankings updated for job {job.id}")
    
    # Step 7: Log Audit Trail
    log_evaluation(
        db,
        application.id,
        job.id,
        candidate.id,
        {
            "rfs": rfs,
            "dcs": dcs,
            "elc": elc,
            "composite": composite,
            "breakdown": breakdown
        },
        fraud_analysis,
        decision,
        decision_reason,
        explanation
    )
    
    print(f"[Pipeline] Evaluation complete for application {application.id}")
    
    return application


def update_application_rankings(db, job_id: int):
    """
    Update rankings for all applications to a specific job
    Rank by composite score (highest to lowest)
    
    Args:
        db: Database session
        job_id: Job ID to update rankings for
    """
    # Get all non-fraud applications for this job, ordered by composite score
    applications = db.query(Application).filter(
        Application.job_id == job_id,
        Application.fraud_flag == False
    ).order_by(desc(Application.composite_score)).all()
    
    # Assign ranks
    for rank, application in enumerate(applications, start=1):
        application.rank = rank
    
    db.commit()
    print(f"[Ranking] Updated rankings for {len(applications)} applications")


def get_application_details(db, application_id: int):
    """
    Retrieve complete application details with all scoring and explanation
    
    Args:
        db: Database session
        application_id: Application ID
        
    Returns:
        Dictionary with complete application details
    """
    application = db.query(Application).filter(Application.id == application_id).first()
    
    if not application:
        return {"error": "Application not found"}
    
    # Get related job and candidate
    from ..models.job import Job
    from ..models.candidate import Candidate
    
    job = db.query(Job).filter(Job.id == application.job_id).first()
    candidate = db.query(Candidate).filter(Candidate.id == application.candidate_id).first()
    
    # Get company info
    from ..models.company import Company
    company = db.query(Company).filter(Company.id == job.company_id).first()
    
    return {
        "application": {
            "id": application.id,
            "status": application.status,
            "created_at": application.created_at.isoformat() if application.created_at else None
        },
        "company": {
            "id": company.id,
            "name": company.name
        } if company else None,
        "job": {
            "id": job.id,
            "role": job.role,
            "salary": job.salary,
            "required_experience": job.required_experience
        },
        "candidate": {
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "experience": candidate.experience
        },
        "scores": {
            "rfs": application.rfs,
            "dcs": application.dcs,
            "elc": application.elc,
            "composite_score": application.composite_score
        },
        "skill_match": application.skill_match,
        "experience_details": application.experience_details,
        "fraud_detection": {
            "fraud_flag": application.fraud_flag,
            "similarity_index": application.similarity_index,
            "details": application.fraud_details
        },
        "decision": {
            "final_decision": application.decision,
            "reason": application.decision_reason,
            "explanation": application.explanation
        }
    }

