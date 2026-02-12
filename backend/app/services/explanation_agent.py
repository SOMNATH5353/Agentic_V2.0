"""
Explanation Agent - Generates human-readable explanations for hiring decisions
Provides transparency and interpretability to the AI evaluation process
"""
from typing import Dict, List


class ExplanationAgent:
    """Generates detailed explanations for hiring decisions"""
    
    def generate_decision_explanation(
        self,
        decision: str,
        scores: Dict,
        skill_match: Dict,
        experience_details: Dict,
        fraud_analysis: Dict
    ) -> Dict[str, any]:
        """
        Generate comprehensive explanation for the hiring decision
        
        Args:
            decision: Final decision (Fast-Track Selected, Selected, etc.)
            scores: Dictionary with rfs, dcs, elc, composite
            skill_match: Skill matching details
            experience_details: Experience compatibility details
            fraud_analysis: Fraud detection results
            
        Returns:
            Dictionary with detailed explanation
        """
        explanation = {
            "decision": decision,
            "summary": self._generate_summary(decision, scores),
            "strengths": self._identify_strengths(scores, skill_match, experience_details),
            "weaknesses": self._identify_weaknesses(scores, skill_match, experience_details),
            "key_factors": self._identify_key_factors(decision, scores, fraud_analysis),
            "skill_analysis": self._explain_skills(skill_match),
            "experience_analysis": self._explain_experience(experience_details),
            "fraud_assessment": self._explain_fraud(fraud_analysis),
            "recommendation": self._generate_recommendation(decision, scores, fraud_analysis),
            "confidence_level": self._calculate_confidence(scores, skill_match)
        }
        
        return explanation
    
    def _generate_summary(self, decision: str, scores: Dict) -> str:
        """Generate one-sentence summary of decision"""
        composite = scores.get("composite_score", 0)
        
        summaries = {
            "Fast-Track Selected": f"Exceptional candidate with composite score of {composite:.2f}. Immediate interview recommended.",
            "Selected": f"Strong candidate with composite score of {composite:.2f}. Schedule interview.",
            "Hire-Pooled": f"Moderate match with composite score of {composite:.2f}. Consider for future opportunities.",
            "Rejected": f"Insufficient match with composite score of {composite:.2f}. Does not meet requirements.",
            "Review Required": f"Potential issues detected. Manual review required before proceeding."
        }
        
        return summaries.get(decision, f"Decision: {decision} with score {composite:.2f}")
    
    def _identify_strengths(self, scores: Dict, skill_match: Dict, exp_details: Dict) -> List[str]:
        """Identify candidate strengths"""
        strengths = []
        
        # High RFS
        if scores.get("rfs", 0) >= 0.80:
            strengths.append(f"Excellent role fit with {scores['rfs']:.0%} semantic alignment")
        
        # Strong skill match (use multiple possible keys for compatibility)
        match_pct = skill_match.get("match_percentage") or skill_match.get("overall_match_percentage", 0)
        if match_pct >= 70:
            matched_count = skill_match.get("matched_count", len(skill_match.get("matched_skills", [])))
            strengths.append(f"Strong skill match: {matched_count} required skills present")
        
        # Experience match
        if scores.get("elc", 0) >= 0.8:
            strengths.append(f"Meets experience requirements ({exp_details.get('candidate', 0)} years)")
        
        # Extra relevant skills (support both key names)
        extra_skills = skill_match.get("extra_skills") or skill_match.get("candidate_extras", [])
        if len(extra_skills) > 5:
            strengths.append(f"Additional {len(extra_skills)} relevant skills beyond requirements")
        
        return strengths if strengths else ["Candidate shows basic qualifications"]
    
    def _identify_weaknesses(self, scores: Dict, skill_match: Dict, exp_details: Dict) -> List[str]:
        """Identify candidate weaknesses"""
        weaknesses = []
        
        # Low RFS
        if scores.get("rfs", 0) < 0.60:
            weaknesses.append(f"Limited role alignment ({scores['rfs']:.0%} fit)")
        
        # Missing required skills (prioritize over nice-to-have)
        missing_required = skill_match.get("missing_required", [])
        if len(missing_required) > 0:
            top_missing = missing_required[:3]
            weaknesses.append(f"Missing required skills: {', '.join(top_missing)}")
        else:
            # Fallback to generic missing skills
            missing_skills = skill_match.get("missing_skills", [])
            if len(missing_skills) > 0:
                top_missing = missing_skills[:3]
                weaknesses.append(f"Missing skills: {', '.join(top_missing)}")
        
        # Experience gap
        gap = exp_details.get("gap", 0)
        if gap > 0:
            weaknesses.append(f"Experience gap: {gap} years below requirement")
        elif exp_details.get("overqualified", False):
            weaknesses.append("Significantly overqualified - may affect retention")
        
        # Low skill match (use multiple possible keys)
        match_pct = skill_match.get("match_percentage") or skill_match.get("overall_match_percentage", 0)
        if match_pct < 50:
            weaknesses.append(f"Only {match_pct}% of required skills present")
        
        return weaknesses if weaknesses else ["No significant weaknesses identified"]
    
    def _identify_key_factors(self, decision: str, scores: Dict, fraud_analysis: Dict) -> List[Dict]:
        """Identify key factors influencing the decision"""
        factors = []
        
        # Composite score factor
        composite = scores.get("composite_score", 0)
        factors.append({
            "factor": "Overall Competency",
            "value": f"{composite:.0%}",
            "impact": "high",
            "description": f"Combined evaluation across all criteria"
        })
        
        # Fraud check
        if fraud_analysis.get("fraud_flag", False):
            factors.append({
                "factor": "Fraud Detection",
                "value": fraud_analysis.get("overall_risk", "unknown"),
                "impact": "critical",
                "description": f"Potential duplication detected ({fraud_analysis.get('similarity_index', 0):.0%} similarity)"
            })
        
        # Experience
        elc = scores.get("elc", 0)
        if elc == 0:
            factors.append({
                "factor": "Experience",
                "value": "Insufficient",
                "impact": "high",
                "description": "Does not meet minimum experience requirement"
            })
        
        # Skill match
        dcs = scores.get("dcs", 0)
        factors.append({
            "factor": "Skill Match",
            "value": f"{dcs:.0%}",
            "impact": "high" if dcs >= 0.7 else "medium",
            "description": "Technical competency alignment"
        })
        
        return factors
    
    def _explain_skills(self, skill_match: Dict) -> Dict:
        """Generate detailed skill analysis explanation"""
        matched = skill_match.get("matched_skills", [])
        missing = skill_match.get("missing_skills", [])
        extra = skill_match.get("extra_skills") or skill_match.get("candidate_extras", [])
        match_pct = skill_match.get("match_percentage") or skill_match.get("overall_match_percentage", 0)
        total_jd = skill_match.get("total_jd_skills") or len(matched) + len(missing)
        total_resume = skill_match.get("total_resume_skills", 0)
        
        return {
            "match_percentage": match_pct,
            "matched_skills": matched[:10],  # Top 10
            "missing_skills": missing[:10],
            "extra_skills": extra[:10],
            "total_required": total_jd,
            "total_candidate": total_resume,
            "analysis": self._skill_analysis_text(skill_match)
        }
    
    def _skill_analysis_text(self, skill_match: Dict) -> str:
        """Generate natural language skill analysis"""
        match_pct = skill_match.get("match_percentage") or skill_match.get("overall_match_percentage", 0)
        matched_count = skill_match.get("matched_count", len(skill_match.get("matched_skills", [])))
        total_required = skill_match.get("total_jd_skills") or (matched_count + len(skill_match.get("missing_skills", [])))
        
        if match_pct >= 80:
            return f"Excellent skill coverage: {matched_count} of {total_required} required skills demonstrated."
        elif match_pct >= 60:
            return f"Good skill coverage: {matched_count} of {total_required} required skills present."
        elif match_pct >= 40:
            return f"Moderate skill coverage: {matched_count} of {total_required} required skills found."
        else:
            return f"Limited skill coverage: Only {matched_count} of {total_required} required skills identified."
    
    def _explain_experience(self, exp_details: Dict) -> Dict:
        """Generate detailed experience explanation"""
        required = exp_details.get("required", 0)
        candidate = exp_details.get("candidate", 0)
        gap = exp_details.get("gap", 0)
        
        if candidate >= required:
            status = "Meets or exceeds requirements"
        elif candidate >= required * 0.75:
            status = "Close to requirements"
        else:
            status = "Below requirements"
        
        return {
            "required_years": required,
            "candidate_years": candidate,
            "gap_years": gap,
            "status": status,
            "overqualified": exp_details.get("overqualified", False),
            "underqualified": exp_details.get("underqualified", False),
            "match_percentage": exp_details.get("percentage_match", 0)
        }
    
    def _explain_fraud(self, fraud_analysis: Dict) -> Dict:
        """Generate fraud detection explanation"""
        if not fraud_analysis:
            return {"status": "clean", "message": "No fraud indicators detected"}
        
        fraud_flag = fraud_analysis.get("fraud_flag", False)
        risk_level = fraud_analysis.get("overall_risk", "low")
        risk_factors = fraud_analysis.get("risk_factors", [])
        
        if not fraud_flag:
            return {
                "status": "clean",
                "risk_level": "none",
                "message": "No fraud indicators detected"
            }
        
        messages = []
        if "high_embedding_similarity" in risk_factors:
            sim = fraud_analysis.get("similarity_index", 0)
            messages.append(f"High similarity to existing resume ({sim:.0%})")
        
        if "text_duplication" in risk_factors:
            messages.append("Potential text duplication detected")
        
        if "email_duplication" in risk_factors:
            messages.append("Email address already exists in system")
        
        if "template_placeholder" in risk_factors:
            messages.append("Resume contains template placeholders")
        
        return {
            "status": "flagged",
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "messages": messages,
            "recommendation": "Manual review required" if risk_level in ["high", "medium"] else "Proceed with caution"
        }
    
    def _generate_recommendation(self, decision: str, scores: Dict, fraud_analysis: Dict) -> str:
        """Generate actionable recommendation"""
        if fraud_analysis.get("fraud_flag", False) and fraud_analysis.get("overall_risk") == "high":
            return "⚠️ Manual review required before proceeding. Potential fraud detected."
        
        recommendations = {
            "Fast-Track Selected": "✅ Immediately schedule interview. Excellent candidate match.",
            "Selected": "✅ Schedule interview. Strong alignment with requirements.",
            "Hire-Pooled": "📋 Add to talent pool for future consideration.",
            "Rejected": "❌ Not recommended for this position.",
            "Review Required": "⚠️ Manual review needed before making final decision."
        }
        
        return recommendations.get(decision, "Review application manually.")
    
    def _calculate_confidence(self, scores: Dict, skill_match: Dict) -> Dict:
        """Calculate confidence level in the decision"""
        composite = scores.get("composite_score", 0)
        match_pct = skill_match.get("match_percentage") or skill_match.get("overall_match_percentage", 0)
        
        # High confidence if scores are clear and decisive
        if composite >= 0.85 or composite <= 0.50:
            confidence = "high"
            confidence_score = 0.9
        elif composite >= 0.75 or composite <= 0.60:
            confidence = "medium"
            confidence_score = 0.7
        else:
            confidence = "low"
            confidence_score = 0.5
        
        # Adjust based on skill match clarity
        if match_pct >= 80 or match_pct <= 30:
            confidence_score += 0.05
        
        return {
            "level": confidence,
            "score": min(round(confidence_score, 2), 1.0),
            "explanation": f"Decision confidence based on score clarity and skill alignment"
        }
    
    def generate_comparison_report(self, applications: List[Dict]) -> Dict:
        """Generate comparative analysis of multiple applications"""
        if not applications:
            return {"error": "No applications to compare"}
        
        sorted_apps = sorted(applications, key=lambda x: x.get("composite_score", 0), reverse=True)
        
        return {
            "total_applications": len(applications),
            "top_candidates": sorted_apps[:5],
            "distribution": {
                "fast_track": sum(1 for a in applications if a.get("decision") == "Fast-Track Selected"),
                "selected": sum(1 for a in applications if a.get("decision") == "Selected"),
                "hire_pooled": sum(1 for a in applications if a.get("decision") == "Hire-Pooled"),
                "rejected": sum(1 for a in applications if a.get("decision") == "Rejected"),
            },
            "average_score": sum(a.get("composite_score", 0) for a in applications) / len(applications),
            "fraud_flagged": sum(1 for a in applications if a.get("fraud_flag", False))
        }


# Singleton instance
explanation_agent = ExplanationAgent()


def explain_decision(decision: str, scores: Dict, skill_match: Dict, 
                     experience_details: Dict, fraud_analysis: Dict) -> Dict:
    """Generate explanation for a hiring decision"""
    return explanation_agent.generate_decision_explanation(
        decision, scores, skill_match, experience_details, fraud_analysis
    )
