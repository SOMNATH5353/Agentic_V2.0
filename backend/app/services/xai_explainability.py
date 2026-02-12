"""
XAI (Explainable AI) Service
Provides detailed, transparent explanations for hiring decisions
"""
from typing import Dict, List, Any
import json


def generate_xai_explanation(
    decision: str,
    scores: Dict[str, float],
    skill_match: Dict,
    experience_details: Dict,
    fraud_analysis: Dict,
    skill_gap: Dict = None
) -> Dict[str, Any]:
    """
    Generate comprehensive XAI explanation for hiring decision
    
    Returns detailed breakdown of:
    - Why this decision was made
    - What factors contributed
    - What could be improved
    - Transparency into the algorithm
    """
    
    explanation = {
        "decision": decision,
        "confidence_level": _calculate_confidence(scores, fraud_analysis),
        "key_factors": _identify_key_factors(scores, skill_match, experience_details, fraud_analysis),
        "strengths": _identify_strengths(scores, skill_match, experience_details),
        "areas_for_improvement": _identify_weaknesses(scores, skill_match, experience_details, skill_gap),
        "score_breakdown": _detailed_score_breakdown(scores),
        "skill_analysis": _skill_analysis_explanation(skill_match, skill_gap),
        "experience_analysis": _experience_explanation(experience_details),
        "fraud_check_explanation": _fraud_explanation(fraud_analysis),
        "decision_rationale": _generate_decision_rationale(decision, scores, skill_match, experience_details, fraud_analysis),
        "recommendations": _generate_recommendations(decision, scores, skill_match, experience_details)
    }
    
    return explanation


def _calculate_confidence(scores: Dict, fraud_analysis: Dict) -> str:
    """Calculate confidence level in the decision"""
    composite = scores.get("composite_score", 0)
    fraud_flag = fraud_analysis.get("fraud_flag", False)
    
    if fraud_flag:
        return "High - Fraud Detected"
    elif composite >= 0.85:
        return "Very High - Strong Match"
    elif composite >= 0.70:
        return "High - Good Match"
    elif composite >= 0.50:
        return "Medium - Moderate Match"
    else:
        return "High - Clear Mismatch"


def _identify_key_factors(scores: Dict, skill_match: Dict, exp_details: Dict, fraud: Dict) -> List[Dict]:
    """Identify the most important factors in the decision"""
    factors = []
    
    # Fraud
    if fraud.get("fraud_flag"):
        factors.append({
            "factor": "Fraud Detection",
            "impact": "Critical",
            "description": f"Detected {fraud.get('similarity_index', 0):.1%} similarity with existing applications",
            "weight": "Automatic Disqualification"
        })
    
    # Skill Match
    skill_score = skill_match.get("match_score", 0)
    if skill_score >= 0.8:
        factors.append({
            "factor": "Excellent Skill Match",
            "impact": "Very Positive",
            "description": f"{skill_score:.1%} of required skills present",
            "weight": "40% of total score"
        })
    elif skill_score < 0.5:
        factors.append({
            "factor": "Skill Gap",
            "impact": "Negative",
            "description": f"Only {skill_score:.1%} of required skills present",
            "weight": "40% of total score"
        })
    
    # Experience
    exp_match = exp_details.get("percentage_match", 0) / 100
    if exp_match >= 1.0:
        factors.append({
            "factor": "Experience Match",
            "impact": "Positive",
            "description": f"Candidate has {exp_details.get('candidate', 0)} years (requires {exp_details.get('required', 0)})",
            "weight": "20% of total score"
        })
    elif exp_match < 0.75:
        factors.append({
            "factor": "Experience Gap",
            "impact": "Negative",
            "description": f"Candidate has {exp_details.get('candidate', 0)} years (requires {exp_details.get('required', 0)})",
            "weight": "20% of total score"
        })
    
    # Role Fit
    rfs = scores.get("rfs", 0)
    if rfs >= 0.8:
        factors.append({
            "factor": "Strong Semantic Alignment",
            "impact": "Very Positive",
            "description": f"Resume and JD have {rfs:.1%} semantic similarity",
            "weight": "40% of total score"
        })
    
    return factors[:5]  # Top 5 factors


def _identify_strengths(scores: Dict, skill_match: Dict, exp_details: Dict) -> List[str]:
    """Identify candidate strengths"""
    strengths = []
    
    if scores.get("rfs", 0) >= 0.75:
        strengths.append(f"Strong resume-role alignment ({scores['rfs']:.1%})")
    
    if scores.get("dcs", 0) >= 0.75:
        strengths.append(f"Excellent technical skill match ({scores['dcs']:.1%})")
    
    if exp_details.get("percentage_match", 0) >= 100:
        years = exp_details.get("candidate", 0)
        strengths.append(f"Meets experience requirement ({years} years)")
    
    matched_skills = skill_match.get("matched_skills", [])
    if len(matched_skills) >= 5:
        strengths.append(f"Possesses {len(matched_skills)} key required skills")
    
    if scores.get("composite_score", 0) >= 0.80:
        strengths.append("Overall strong candidate profile")
    
    return strengths


def _identify_weaknesses(scores: Dict, skill_match: Dict, exp_details: Dict, skill_gap: Dict = None) -> List[str]:
    """Identify areas for improvement"""
    weaknesses = []
    
    if scores.get("rfs", 0) < 0.60:
        weaknesses.append(f"Low semantic alignment with role ({scores['rfs']:.1%})")
    
    if scores.get("dcs", 0) < 0.60:
        weaknesses.append(f"Skill gap in technical requirements ({scores['dcs']:.1%})")
    
    if exp_details.get("underqualified", False):
        gap = abs(exp_details.get("gap", 0))
        weaknesses.append(f"Needs {gap} more years of experience")
    
    if skill_gap:
        missing = skill_gap.get("missing_skills", [])
        if len(missing) > 0:
            weaknesses.append(f"Missing {len(missing)} critical skills: {', '.join(missing[:3])}")
    
    return weaknesses


def _detailed_score_breakdown(scores: Dict) -> Dict:
    """Provide transparent score breakdown"""
    breakdown = scores.get("breakdown", {})
    
    return {
        "composite_score": {
            "value": scores.get("composite_score", 0),
            "percentage": f"{scores.get('composite_score', 0):.1%}",
            "interpretation": _interpret_score(scores.get("composite_score", 0))
        },
        "role_fit_score": {
            "value": scores.get("rfs", 0),
            "percentage": f"{scores.get('rfs', 0):.1%}",
            "weight": "40%",
            "contribution": breakdown.get("rfs_contribution", 0),
            "interpretation": _interpret_score(scores.get("rfs", 0))
        },
        "domain_competency_score": {
            "value": scores.get("dcs", 0),
            "percentage": f"{scores.get('dcs', 0):.1%}",
            "weight": "40%",
            "contribution": breakdown.get("dcs_contribution", 0),
            "interpretation": _interpret_score(scores.get("dcs", 0))
        },
        "experience_compatibility": {
            "value": scores.get("elc", 0),
            "percentage": f"{scores.get('elc', 0):.1%}",
            "weight": "20%",
            "contribution": breakdown.get("elc_contribution", 0),
            "interpretation": _interpret_score(scores.get("elc", 0))
        }
    }


def _interpret_score(score: float) -> str:
    """Interpret what a score means"""
    if score >= 0.90:
        return "Exceptional"
    elif score >= 0.80:
        return "Excellent"
    elif score >= 0.70:
        return "Good"
    elif score >= 0.60:
        return "Fair"
    elif score >= 0.50:
        return "Moderate"
    else:
        return "Needs Improvement"


def _skill_analysis_explanation(skill_match: Dict, skill_gap: Dict = None) -> Dict:
    """Detailed skill analysis explanation"""
    matched = skill_match.get("matched_skills", [])
    missing = skill_match.get("missing_skills", [])
    extra = skill_match.get("candidate_extras", [])
    
    analysis = {
        "overall_match": f"{skill_match.get('match_score', 0):.1%}",
        "matched_skills": {
            "count": len(matched),
            "skills": matched,
            "impact": "These skills directly align with job requirements"
        },
        "missing_skills": {
            "count": len(missing),
            "skills": missing,
            "impact": "Learning these skills would improve candidacy",
            "criticality": _assess_skill_criticality(missing, skill_match)
        },
        "additional_skills": {
            "count": len(extra),
            "skills": extra[:10],  # Top 10
            "impact": "Bonus skills that add value beyond requirements"
        }
    }
    
    if skill_gap:
        analysis["skill_gap_details"] = skill_gap
    
    return analysis


def _assess_skill_criticality(missing_skills: List[str], skill_match: Dict) -> str:
    """Assess how critical missing skills are"""
    if len(missing_skills) == 0:
        return "None - All required skills present"
    
    total_required = skill_match.get("jd_skill_count", 1)
    missing_ratio = len(missing_skills) / total_required if total_required > 0 else 1
    
    if missing_ratio >= 0.7:
        return "High - Most required skills are missing"
    elif missing_ratio >= 0.4:
        return "Medium - Several key skills are missing"
    else:
        return "Low - Only some skills are missing"


def _experience_explanation(exp_details: Dict) -> Dict:
    """Detailed experience analysis"""
    required = exp_details.get("required", 0)
    candidate = exp_details.get("candidate", 0)
    gap = exp_details.get("gap", 0)
    
    if candidate >= required:
        status = "Meets Requirement"
        detail = f"Candidate has {candidate} years, exceeding the {required} year requirement"
    elif candidate >= required * 0.75:
        status = "Nearly Meets Requirement"
        detail = f"Candidate has {candidate} years, approaching the {required} year requirement"
    else:
        status = "Below Requirement"
        detail = f"Candidate has {candidate} years, {abs(gap)} years short of the {required} year requirement"
    
    return {
        "required_years": required,
        "candidate_years": candidate,
        "gap_years": gap,
        "status": status,
        "explanation": detail,
        "percentage_match": exp_details.get("percentage_match", 0),
        "overqualified": exp_details.get("overqualified", False),
        "underqualified": exp_details.get("underqualified", False)
    }


def _fraud_explanation(fraud_analysis: Dict) -> Dict:
    """Explain fraud detection results"""
    fraud_flag = fraud_analysis.get("fraud_flag", False)
    similarity = fraud_analysis.get("similarity_index", 0)
    
    return {
        "fraud_detected": fraud_flag,
        "similarity_to_existing": f"{similarity:.1%}",
        "status": "FRAUD DETECTED - Application Flagged" if fraud_flag else "Clean - No fraud detected",
        "checks_performed": [
            "Resume duplication analysis",
            "Email pattern analysis",
            "Content similarity check"
        ],
        "explanation": fraud_analysis.get("fraud_explanation", "Standard fraud checks passed") if fraud_flag 
                      else "Application passed all fraud detection checks"
    }


def _generate_decision_rationale(decision: str, scores: Dict, skill_match: Dict, 
                                exp_details: Dict, fraud: Dict) -> str:
    """Generate human-readable decision rationale"""
    composite = scores.get("composite_score", 0)
    skill_score = skill_match.get("match_score", 0)
    
    if fraud.get("fraud_flag"):
        return (f"Application REJECTED due to fraud detection. The system identified "
                f"{fraud.get('similarity_index', 0):.1%} similarity with existing applications, "
                f"indicating potential resume duplication or fraudulent submission.")
    
    if decision == "Fast-Track Selected":
        return (f"Candidate FAST-TRACKED for immediate interview. Exceptional performance with "
                f"{composite:.1%} overall match, {skill_score:.1%} skill alignment, and strong "
                f"experience fit. This candidate exceeds all requirements and represents a top-tier match.")
    
    elif decision == "Selected":
        return (f"Candidate SELECTED for interview round. Strong performance with {composite:.1%} "
                f"overall match. The candidate demonstrates {skill_score:.1%} skill alignment and "
                f"meets the core requirements for this role.")
    
    elif decision == "Hire-Pooled":
        return (f"Candidate placed in TALENT POOL for future consideration. Shows potential with "
                f"{composite:.1%} overall match. While not an immediate fit, the candidate has "
                f"transferable skills and could be valuable for future opportunities.")
    
    elif decision == "Review Required":
        return (f"MANUAL REVIEW REQUIRED. The candidate shows mixed signals - some areas of strength "
                f"but also notable gaps. Human review recommended to make final decision.")
    
    else:  # Rejected
        return (f"Candidate NOT SELECTED for this position. With {composite:.1%} overall match and "
                f"{skill_score:.1%} skill alignment, the candidate does not meet the minimum "
                f"requirements for this role at this time.")


def _generate_recommendations(decision: str, scores: Dict, skill_match: Dict, 
                             exp_details: Dict) -> List[str]:
    """Generate actionable recommendations"""
    recommendations = []
    
    if decision in ["Fast-Track Selected", "Selected"]:
        recommendations.append("Proceed with scheduling interview")
        recommendations.append("Prepare technical assessment based on matched skills")
        recommendations.append("Verify experience claims during interview")
    
    elif decision == "Hire-Pooled":
        recommendations.append("Keep candidate in talent pool for 6 months")
        recommendations.append("Consider for related roles or future openings")
        missing = skill_match.get("missing_skills", [])
        if missing:
            recommendations.append(f"If candidate learns {', '.join(missing[:3])}, reconsider application")
    
    elif decision == "Rejected":
        recommendations.append("Send polite rejection email")
        recommendations.append("Consider candidate for other open positions if any align better")
        missing = skill_match.get("missing_skills", [])
        if missing:
            recommendations.append(f"Candidate could reapply after gaining: {', '.join(missing[:3])}")
    
    return recommendations
