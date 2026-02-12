"""
Enhanced Scoring Engine with Skill-Based Matching
"""
from ..utils.similarity import cosine_similarity
from .inference_engine import extract_skills_from_text, compute_skill_similarity, inference_engine
from typing import Dict, Tuple, List
import json


def compute_rfs(jd_emb: List[float], resume_emb: List[float]) -> float:
    """
    Role Fit Score: Semantic similarity between JD and Resume
    Higher score = better semantic alignment
    """
    return round(cosine_similarity(jd_emb, resume_emb), 4)


def compute_dcs(jd_text: str, resume_text: str, jd_skills: List[str] = None, 
                resume_skills: List[str] = None, use_weighted: bool = True) -> Tuple[float, Dict]:
    """
    Domain Competency Score: Actual skill matching (TECHNICAL SKILLS ONLY)
    
    NOTE: Only evaluates technical skills. Soft skills (leadership, communication, etc.)
    are excluded from scoring to avoid unfair penalties.
    
    NOW WITH WEIGHTED SCORING: Required skills count more than nice-to-have skills!
    
    Args:
        jd_text: Job description text
        resume_text: Resume text
        jd_skills: Pre-extracted JD technical skills (optional)
        resume_skills: Pre-extracted resume technical skills (optional)
        use_weighted: Use weighted scoring based on required vs nice-to-have (default: True)
        
    Returns:
        Tuple of (dcs_score, skill_details)
    """
    # Extract skills if not provided
    if jd_skills is None:
        jd_skill_data = extract_skills_from_text(jd_text)
        # Use ONLY technical skills for DCS, not soft skills
        jd_skills = jd_skill_data["technical_skills"]
    
    if resume_skills is None:
        resume_skill_data = extract_skills_from_text(resume_text)
        # Use ONLY technical skills for DCS, not soft skills
        resume_skills = resume_skill_data["technical_skills"]
    
    # Use weighted skill matching if enabled (default)
    if use_weighted:
        skill_match = inference_engine.compute_weighted_skill_match(jd_text, jd_skills, resume_skills)
        dcs_score = skill_match["match_score"]
    else:
        # Original unweighted matching
        skill_match = compute_skill_similarity(jd_skills, resume_skills)
        dcs_score = skill_match["match_score"]
    
    return round(dcs_score, 4), skill_match


def compute_elc(required_exp: int, candidate_exp: int, jd_text: str = "", 
                resume_text: str = "") -> Tuple[float, Dict]:
    """
    Experience Level Compatibility: Enhanced experience matching
    
    Args:
        required_exp: Required experience from JD
        candidate_exp: Candidate's experience
        jd_text: JD text for additional analysis (optional)
        resume_text: Resume text for additional analysis (optional)
        
    Returns:
        Tuple of (elc_score, experience_details)
    """
    # Base calculation
    if candidate_exp >= required_exp:
        base_score = 1.0
    elif candidate_exp >= required_exp * 0.75:
        base_score = 0.8  # Within 75% of requirement
    elif candidate_exp >= required_exp * 0.5:
        base_score = 0.5  # Within 50% of requirement
    else:
        base_score = 0.0  # Significantly under-qualified
    
    # Penalty for massive overqualification (may lead to retention issues)
    if candidate_exp > required_exp * 2.5:
        base_score *= 0.9  # Slight penalty for overqualification
    
    experience_details = {
        "required": required_exp,
        "candidate": candidate_exp,
        "gap": required_exp - candidate_exp,
        "percentage_match": round((min(candidate_exp, required_exp) / max(required_exp, 1)) * 100, 2),
        "overqualified": candidate_exp > required_exp * 2,
        "underqualified": candidate_exp < required_exp * 0.75
    }
    
    return round(base_score, 4), experience_details


def compute_composite(rfs: float, dcs: float, elc: float, 
                      weights: Dict[str, float] = None) -> Tuple[float, Dict]:
    """
    Composite Score: Weighted combination of all metrics
    
    Default weights:
    - RFS (Role Fit): 40% - Semantic alignment
    - DCS (Domain Competency): 40% - Actual skill match
    - ELC (Experience): 20% - Experience compatibility
    
    Args:
        rfs: Role Fit Score
        dcs: Domain Competency Score
        elc: Experience Level Compatibility
        weights: Custom weights (optional)
        
    Returns:
        Tuple of (composite_score, breakdown)
    """
    if weights is None:
        weights = {
            "rfs": 0.40,
            "dcs": 0.40,
            "elc": 0.20
        }
    
    composite = (
        weights["rfs"] * rfs +
        weights["dcs"] * dcs +
        weights["elc"] * elc
    )
    
    breakdown = {
        "rfs_contribution": round(weights["rfs"] * rfs, 4),
        "dcs_contribution": round(weights["dcs"] * dcs, 4),
        "elc_contribution": round(weights["elc"] * elc, 4),
        "weights": weights,
        "total": round(composite, 4)
    }
    
    return round(composite, 4), breakdown


def compute_all_scores(job, candidate) -> Dict:
    """
    Compute all scoring metrics for a job-candidate pair
    
    Args:
        job: Job model instance with jd_text, jd_embedding, and skills_extracted
        candidate: Candidate model instance with resume_text, resume_embedding, and skills_extracted
        
    Returns:
        Dictionary with all scores and details
    """
    # Use pre-stored skills if available (with inference and normalization already applied),
    # otherwise extract fresh from text
    if hasattr(job, 'skills_extracted') and job.skills_extracted:
        jd_skill_data = job.skills_extracted
    else:
        jd_skill_data = extract_skills_from_text(job.jd_text)
    
    if hasattr(candidate, 'skills_extracted') and candidate.skills_extracted:
        resume_skill_data = candidate.skills_extracted
    else:
        resume_skill_data = extract_skills_from_text(candidate.resume_text)
    
    # Compute RFS
    rfs = compute_rfs(job.jd_embedding, candidate.resume_embedding)
    
    # Compute DCS with skill details (TECHNICAL SKILLS ONLY)
    dcs, skill_match = compute_dcs(
        job.jd_text, 
        candidate.resume_text,
        jd_skill_data["technical_skills"],  # Only technical skills for scoring
        resume_skill_data["technical_skills"]  # Only technical skills for scoring
    )
    
    # Compute ELC with experience details
    elc, exp_details = compute_elc(
        job.required_experience,
        candidate.experience,
        job.jd_text,
        candidate.resume_text
    )
    
    # Compute composite score
    composite, breakdown = compute_composite(rfs, dcs, elc)
    
    return {
        "rfs": rfs,
        "dcs": dcs,
        "elc": elc,
        "composite_score": composite,
        "breakdown": breakdown,
        "skill_match": skill_match,
        "experience_details": exp_details,
        "jd_skills": jd_skill_data,
        "resume_skills": resume_skill_data
    }

