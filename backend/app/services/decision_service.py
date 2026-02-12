"""
Enhanced Decision Service with Multi-Factor Analysis
"""
from typing import Tuple, Dict


def make_decision(
    rfs: float,
    dcs: float,
    elc: float,
    composite: float,
    fraud_flag: bool,
    sim_index: float,
    fraud_details: Dict = None,
    skill_match: Dict = None,
    exp_details: Dict = None
) -> Tuple[str, str]:
    """
    Make hiring decision based on comprehensive evaluation
    
    IMPROVED Decision Thresholds (more fair to candidates):
    - Fast-Track Selected: composite >= 0.85 AND required_skills >= 0.90
    - Selected: composite >= 0.65 AND required_skills >= 0.75
    - Hire-Pooled: composite >= 0.50 OR (required_skills >= 0.60 AND composite >= 0.45)
    - Rejected: composite < 0.45 OR critical issues
    - Review Required: fraud detected OR boundary cases
    
    NOTE: Now considers required vs nice-to-have skills separately!
    Missing nice-to-have skills won't heavily penalize candidates.
    
    Args:
        rfs: Role Fit Score
        dcs: Domain Competency Score
        elc: Experience Level Compatibility
        composite: Composite score
        fraud_flag: Fraud detection flag
        sim_index: Similarity index
        fraud_details: Detailed fraud analysis (optional)
        skill_match: Skill matching details (optional)
        exp_details: Experience details (optional)
        
    Returns:
        Tuple of (decision, reason)
    """
    # Extract required skill match if available
    required_skill_match = 0.0
    if skill_match and "required_match_score" in skill_match:
        required_skill_match = skill_match["required_match_score"]
        matched_required = skill_match.get("matched_required", [])
        missing_required = skill_match.get("missing_required", [])
    else:
        # Fallback to regular match score
        required_skill_match = dcs
        matched_required = skill_match.get("matched_skills", []) if skill_match else []
        missing_required = skill_match.get("missing_skills", []) if skill_match else []
    # Critical Fraud Check
    if fraud_flag and sim_index > 0.92:
        return "Review Required", "Critical: High resume similarity detected (>92%). Manual review required."
    
    # High-risk fraud
    if fraud_details and fraud_details.get("overall_risk") == "high":
        risk_factors = fraud_details.get("risk_factors", [])
        return "Review Required", f"Fraud indicators: {', '.join(risk_factors)}. Requires verification."
    
    # Experience Disqualification (more lenient)
    if elc < 0.3:  # Only reject if severely under-qualified
        gap = exp_details.get("gap", 0) if exp_details else 0
        if gap > 0:
            return "Rejected", f"Insufficient experience: {gap} years below requirement."
    
    # Medium-risk fraud but good scores
    if fraud_flag and sim_index > 0.85 and composite >= 0.70:
        return "Review Required", f"Good qualifications but moderate similarity detected ({sim_index:.0%}). Verify uniqueness."
    
    # Excellent Candidate (with focus on required skills)
    if composite >= 0.85 and required_skill_match >= 0.85:
        strengths = []
        if rfs >= 0.85:
            strengths.append("excellent role fit")
        if required_skill_match >= 0.85:
            strengths.append("strong match on required skills")
        if elc >= 0.8:
            strengths.append("appropriate experience")
        
        reason = f"Outstanding candidate: {', '.join(strengths) if strengths else 'all metrics exceed threshold'}. Matches {len(matched_required)} required skills."
        return "Fast-Track Selected", reason
    
    # Strong Candidate (more achievable threshold)
    if (composite >= 0.65 and required_skill_match >= 0.75) or (composite >= 0.75 and required_skill_match >= 0.65):
        matched_count = len(matched_required)
        missing_count = len(missing_required)
        
        if missing_count <= 2:
            reason = f"Strong alignment ({composite:.0%}). Matches {matched_count} required skills, missing only {missing_count}."
        else:
            reason = f"Good alignment ({composite:.0%}). Matches {matched_count}/{matched_count + missing_count} required skills."
        
        return "Selected", reason
    
    # Moderate Candidate (more lenient)
    if (composite >= 0.50 and required_skill_match >= 0.60) or (composite >= 0.55 and required_skill_match >= 0.50):
        if fraud_flag:
            return "Review Required", f"Moderate fit but fraud flag raised. Review before pooling."
        
        matched_count = len(matched_required)
        missing_count = len(missing_required)
        
        if required_skill_match >= 0.60:
            reason = f"Moderate potential ({composite:.0%}). Has {matched_count} required skills. Consider for future roles or with training."
        else:
            reason = f"Acceptable foundation. Matches {matched_count} required skills. Could grow into role with mentorship."
        
        return "Hire-Pooled", reason
    
    # Below Threshold (but provide constructive feedback)
    primary_issue = []
    matched_count = len(matched_required)
    missing_count = len(missing_required)
    
    if rfs < 0.50:
        primary_issue.append(f"poor role fit ({rfs:.0%})")
    
    if required_skill_match < 0.50:
        if missing_count > 0:
            primary_issue.append(f"missing {missing_count} required skills ({required_skill_match:.0%} match)")
        else:
            primary_issue.append(f"insufficient required skills match ({required_skill_match:.0%})")
    elif dcs < 0.50:
        # Low overall skill match but decent required skills
        primary_issue.append(f"limited technical breadth (meets core requirements but overall skills low)")
    
    if elc < 0.50:
        gap = exp_details.get("gap", 0) if exp_details else 0
        if gap > 0:
            primary_issue.append(f"insufficient experience ({gap} years below requirement)")
        else:
            primary_issue.append("experience level concerns")
    
    if primary_issue:
        reason = f"Not selected: {', '.join(primary_issue)}. "
        if missing_count > 0 and missing_count <= 5:
            top_missing = missing_required[:3]
            reason += f"Focus on developing: {', '.join(top_missing)}."
        elif required_skill_match >= 0.40:
            reason += "Shows potential - consider reapplying after gaining more experience."
    else:
        reason = f"Overall score ({composite:.0%}) below minimum threshold. Significant gaps in multiple areas."
    
    return "Rejected", reason
