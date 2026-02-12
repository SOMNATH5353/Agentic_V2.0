"""
Skill Gap Analysis and Evidence Graph Generator
Provides detailed skill gap analysis and graph data for visualization
"""
from typing import Dict, List, Any
from collections import defaultdict


def analyze_skill_gap(
    matched_skills: List[str],
    missing_skills: List[str],
    candidate_extras: List[str],
    jd_text: str = "",
    resume_text: str = "",
    skill_match_details: Dict = None
) -> Dict[str, Any]:
    """
    Comprehensive skill gap analysis
    
    NOW ENHANCED: Considers required vs nice-to-have skills separately!
    
    Args:
        matched_skills: Skills that matched
        missing_skills: Skills that are missing
        candidate_extras: Extra skills candidate has
        jd_text: Job description text
        resume_text: Resume text
        skill_match_details: Detailed skill match info with required/nice-to-have breakdown
    
    Returns:
        - Detailed breakdown of skill gaps with priority
        - Severity levels
        - Learning path recommendations
        - Estimated time to close gap
    """
    
    # Extract required vs nice-to-have breakdown if available
    if skill_match_details and "missing_required" in skill_match_details:
        missing_required = skill_match_details.get("missing_required", [])
        missing_nice_to_have = skill_match_details.get("missing_nice_to_have", [])
        matched_required = skill_match_details.get("matched_required", [])
        matched_nice_to_have = skill_match_details.get("matched_nice_to_have", [])
        
        total_required = len(matched_required) + len(missing_required)
        gap_percentage_required = (len(missing_required) / total_required * 100) if total_required > 0 else 0
    else:
        # Fallback to basic categorization
        missing_required = []
        missing_nice_to_have = []
        critical_skills, important_skills, nice_to_have = _categorize_missing_skills(
            missing_skills, jd_text
        )
        missing_required = critical_skills + important_skills
        missing_nice_to_have = nice_to_have
        gap_percentage_required = (len(missing_required) / len(matched_skills + missing_skills) * 100) if (matched_skills or missing_skills) else 0
    
    total_required = len(matched_skills) + len(missing_skills)
    gap_percentage = (len(missing_skills) / total_required * 100) if total_required > 0 else 0
    
    # Categorize missing skills by priority (use enhanced categorization)
    if not missing_required and not missing_nice_to_have:
        # Legacy fallback
        critical_skills, important_skills, nice_to_have = _categorize_missing_skills(
            missing_skills, jd_text
        )
    else:
        # Use the required/nice-to-have breakdown
        critical_skills = missing_required[:len(missing_required)//2] if len(missing_required) > 2 else missing_required
        important_skills = missing_required[len(missing_required)//2:] if len(missing_required) > 2 else []
        nice_to_have = missing_nice_to_have
    
    # Generate learning roadmap
    learning_roadmap = _generate_learning_roadmap(missing_skills)
    
    # Identify transferable skills
    transferable = _identify_transferable_skills(candidate_extras, missing_skills)
    
    # Calculate gap severity (prioritize required skills)
    severity = _calculate_gap_severity(
        len(critical_skills),
        len(important_skills),
        len(nice_to_have),
        gap_percentage_required if 'gap_percentage_required' in locals() else gap_percentage
    )
    
    return {
        "summary": {
            "total_required_skills": total_required,
            "skills_matched": len(matched_skills),
            "skills_missing": len(missing_skills),
            "skills_missing_required": len(missing_required) if missing_required else len(critical_skills + important_skills),
            "skills_missing_nice_to_have": len(missing_nice_to_have) if missing_nice_to_have else len(nice_to_have),
            "gap_percentage": round(gap_percentage, 2),
            "gap_percentage_required": round(gap_percentage_required, 2) if 'gap_percentage_required' in locals() else round(gap_percentage, 2),
            "severity": severity,
            "is_closeable": gap_percentage < 40,  # Gap is closeable if < 40%
            "focus_on_required": len(missing_required) > 0 if missing_required else len(critical_skills + important_skills) > 0
        },
        "gap_breakdown": {
            "critical_missing": {
                "count": len(critical_skills),
                "skills": critical_skills,
                "impact": "High - Essential for role performance (Required Skills)"
            },
            "important_missing": {
                "count": len(important_skills),
                "skills": important_skills,
                "impact": "Medium - Important but can be learned on job (Required Skills)"
            },
            "nice_to_have_missing": {
                "count": len(nice_to_have),
                "skills": nice_to_have,
                "impact": "Low - Beneficial but not critical (Nice-to-Have Skills)"
            }
        },
        "transferable_skills": {
            "count": len(transferable),
            "skills": transferable,
            "impact": "These existing skills can help learn missing ones faster"
        },
        "learning_roadmap": learning_roadmap,
        "estimated_closure_time": _estimate_learning_time(missing_skills),
        "recommendations": _generate_gap_recommendations(
            critical_skills, important_skills, nice_to_have, transferable
        )
    }


def generate_skill_evidence_graph(
    matched_skills: List[str],
    missing_skills: List[str],
    candidate_extras: List[str],
    jd_technical_skills: List[str],
    resume_technical_skills: List[str]
) -> Dict[str, Any]:
    """
    Generate data structure for skill evidence graph visualization
    
    Returns graph data in format suitable for frontend visualization
    (e.g., D3.js, Chart.js, or other graph libraries)
    """
    
    nodes = []
    edges = []
    node_id = 0
    
    # Central node - The Job
    nodes.append({
        "id": "job",
        "label": "Job Requirements",
        "type": "job",
        "size": 30,
        "color": "#3498db"
    })
    
    # Matched skills nodes (Green)
    for skill in matched_skills:
        node_id += 1
        nodes.append({
            "id": f"matched_{node_id}",
            "label": skill,
            "type": "matched",
            "size": 20,
            "color": "#27ae60"  # Green
        })
        edges.append({
            "source": "job",
            "target": f"matched_{node_id}",
            "type": "required",
            "strength": 1.0,
            "color": "#27ae60",
            "label": "Matched"
        })
        edges.append({
            "source": f"matched_{node_id}",
            "target": "candidate",
            "type": "possessed",
            "strength": 1.0,
            "color": "#27ae60"
        })
    
    # Missing skills nodes (Red)
    for skill in missing_skills:
        node_id += 1
        nodes.append({
            "id": f"missing_{node_id}",
            "label": skill,
            "type": "missing",
            "size": 20,
            "color": "#e74c3c"  # Red
        })
        edges.append({
            "source": "job",
            "target": f"missing_{node_id}",
            "type": "required",
           "strength": 0.5,
            "color": "#e74c3c",
            "label": "Missing"
        })
    
    # Candidate extras (Blue)
    for skill in candidate_extras[:10]:  # Limit to top 10 extras
        node_id += 1
        nodes.append({
            "id": f"extra_{node_id}",
            "label": skill,
            "type": "extra",
            "size": 15,
            "color": "#9b59b6"  # Purple
        })
        edges.append({
            "source": "candidate",
            "target": f"extra_{node_id}",
            "type": "possessed",
            "strength": 0.7,
            "color": "#9b59b6",
            "label": "Bonus Skill"
        })
    
    # Central node - The Candidate
    nodes.append({
        "id": "candidate",
        "label": "Candidate Skills",
        "type": "candidate",
        "size": 30,
        "color": "#e67e22"
    })
    
    # Calculate statistics for the graph
    match_rate = len(matched_skills) / (len(matched_skills) + len(missing_skills)) if (len(matched_skills) + len(missing_skills)) > 0 else 0
    
    return {
        "graph": {
            "nodes": nodes,
            "edges": edges
        },
        "statistics": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "matched_skills_count": len(matched_skills),
            "missing_skills_count": len(missing_skills),
            "extra_skills_count": min(len(candidate_extras), 10),
            "match_rate": round(match_rate * 100, 2)
        },
        "legend": {
            "green": "Skills that match job requirements",
            "red": "Skills missing from candidate profile",
            "purple": "Additional skills candidate possesses",
            "blue": "Job requirements node",
            "orange": "Candidate skills node"
        },
        "visualization_config": {
            "layout": "force-directed",
            "show_labels": True,
            "interactive": True,
            "zoom_enabled": True
        }
    }


def _categorize_missing_skills(missing_skills: List[str], jd_text: str = "") -> tuple:
    """Categorize missing skills by priority based on context"""
    
    # Common critical skill keywords
    critical_keywords = [
        'python', 'java', 'javascript', 'sql', 'aws', 'azure', 'kubernetes',
        'react', 'angular', 'node', 'django', 'spring', 'docker'
    ]
    
    critical = []
    important = []
    nice_to_have = []
    
    for skill in missing_skills:
        skill_lower = skill.lower()
        
        # Check if skill appears multiple times in JD (indicates importance)
        if jd_text and jd_text.lower().count(skill_lower) >= 3:
            critical.append(skill)
        elif any(keyword in skill_lower for keyword in critical_keywords):
            important.append(skill)
        else:
            nice_to_have.append(skill)
    
    return critical, important, nice_to_have


def _identify_transferable_skills(candidate_extras: List[str], missing_skills: List[str]) -> List[Dict]:
    """Identify skills candidate has that could transfer to missing skills"""
    
    # Skill relationship mapping (simplified)
    skill_relationships = {
        'python': ['java', 'javascript', 'ruby', 'go'],
        'java': ['python', 'c++', 'c#', 'kotlin'],
        'javascript': ['typescript', 'node.js', 'react', 'vue'],
        'react': ['angular', 'vue', 'svelte'],
        'aws': ['azure', 'gcp', 'cloud'],
        'postgresql': ['mysql', 'mongodb', 'sql'],
        'docker': ['kubernetes', 'containerization']
    }
    
    transferable = []
    
    for extra in candidate_extras:
        extra_lower = extra.lower()
        for missing in missing_skills:
            missing_lower = missing.lower()
            
            # Check if candidate skill can transfer to missing skill
            if extra_lower in skill_relationships:
                if any(related in missing_lower for related in skill_relationships[extra_lower]):
                    transferable.append({
                        "from_skill": extra,
                        "to_skill": missing,
                        "transfer_ease": "Easy - Related technology"
                    })
    
    return transferable


def _generate_learning_roadmap(missing_skills: List[str]) -> List[Dict]:
    """Generate a learning roadmap for missing skills"""
    
    # Skill learning time estimates (in weeks)
    learning_times = {
        'basic': 4,
        'intermediate': 8,
        'advanced': 16,
        'expert': 24
    }
    
    roadmap = []
    
    for i, skill in enumerate(missing_skills[:10]):  # Top 10 skills
        # Estimate difficulty based on skill type (simplified)
        skill_lower = skill.lower()
        
        if any(x in skill_lower for x in ['expert', 'senior', 'architect']):
            difficulty = 'advanced'
            time_weeks = learning_times['advanced']
        elif any(x in skill_lower for x in ['aws', 'kubernetes', 'microservices']):
            difficulty = 'intermediate'
            time_weeks = learning_times['intermediate']
        else:
            difficulty = 'basic'
            time_weeks = learning_times['basic']
        
        roadmap.append({
            "priority": i + 1,
            "skill": skill,
            "difficulty": difficulty,
            "estimated_weeks": time_weeks,
            "learning_resources": [
                f"Online courses for {skill}",
                f"Official {skill} documentation",
                f"Practice projects using {skill}"
            ]
        })
    
    return roadmap


def _calculate_gap_severity(critical: int, important: int, nice_to_have: int, gap_pct: float) -> str:
    """Calculate overall gap severity"""
    
    if critical >= 5 or gap_pct >= 70:
        return "Critical - Major skills gap"
    elif critical >= 2 or gap_pct >= 50:
        return "High - Significant skills gap"
    elif important >= 5 or gap_pct >= 30:
        return "Medium - Moderate skills gap"
    elif gap_pct >= 15:
        return "Low - Minor skills gap"
    else:
        return "Minimal - Negligible skills gap"


def _estimate_learning_time(missing_skills: List[str]) -> Dict:
    """Estimate time to close skill gap"""
    
    # Average 6 weeks per skill (simplified estimate)
    weeks_per_skill = 6
    total_skills = len(missing_skills)
    
    # Account for parallel learning
    if total_skills <= 2:
        total_weeks = total_skills * weeks_per_skill
    else:
        # Assume some parallel learning
        total_weeks = (total_skills * weeks_per_skill) * 0.7
    
    months = total_weeks / 4
    
    return {
        "total_weeks": int(total_weeks),
        "total_months": round(months, 1),
        "skills_count": total_skills,
        "assumptions": [
            "Assumes dedicated learning time",
            "Some skills can be learned in parallel",
            "Prior experience accelerates learning"
        ]
    }


def _generate_gap_recommendations(critical: List, important: List, nice_to_have: List, 
                                  transferable: List) -> List[str]:
    """Generate actionable recommendations for closing skill gap"""
    
    recommendations = []
    
    if len(critical) > 0:
        recommendations.append(f"PRIORITY: Focus on learning critical skills: {', '.join(critical[:3])}")
    
    if len(transferable) > 0:
        recommendations.append(f"Leverage existing skills ({transferable[0]['from_skill']}) to learn {transferable[0]['to_skill']} faster")
    
    if len(important) > 0:
        recommendations.append(f"Next, work on important skills: {', '.join(important[:3])}")
    
    if len(nice_to_have) > 0:
        recommendations.append(f"Optional: Add value with: {', '.join(nice_to_have[:2])}")
    
    recommendations.append("Consider bootcamps, online courses, or certification programs")
    recommendations.append("Build portfolio projects demonstrating newly learned skills")
    
    return recommendations
