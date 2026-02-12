# Advanced Analytics & Explainability Features - API Documentation

## New Features Added

### 1. **Candidate Ranking System**
Automatically ranks all applicants for each job based on composite scores.

### 2. **XAI (Explainable AI)**
Provides transparent, detailed explanations for hiring decisions.

### 3. **Skill Gap Analysis**
Analyzes the gap between candidate skills and job requirements with learning roadmaps.

### 4. **Skill Evidence Graph**
Visual graph data showing skill matches for frontend visualization.

---

## Analytics Endpoints

### 1. Get XAI Explanation
**Endpoint:** `GET /analytics/application/{application_id}/xai`

**Description:** Get comprehensive explainable AI insights for an application decision.

**Response:**
```json
{
  "application_id": 1,
  "candidate": {
    "name": "John Doe",
    "experience": 5
  },
  "job": {
    "role": "Senior Software Engineer",
    "required_experience": 5
  },
  "xai_explanation": {
    "decision": "Selected",
    "confidence_level": "High - Good Match",
    "key_factors": [
      {
        "factor": "Excellent Skill Match",
        "impact": "Very Positive",
        "description": "85.0% of required skills present",
        "weight": "40% of total score"
      }
    ],
    "strengths": [
      "Strong resume-role alignment (82.5%)",
      "Excellent technical skill match (85.0%)"
    ],
    "areas_for_improvement": [
      "Missing 3 critical skills: Kubernetes, AWS, Docker"
    ],
    "score_breakdown": {
      "composite_score": {
        "value": 0.78,
        "percentage": "78.0%",
        "interpretation": "Good"
      }
    },
    "decision_rationale": "Candidate SELECTED for interview round...",
    "recommendations": [
      "Proceed with scheduling interview",
      "Prepare technical assessment based on matched skills"
    ]
  }
}
```

---

### 2. Get Skill Gap Analysis
**Endpoint:** `GET /analytics/application/{application_id}/skill-gap`

**Description:** Get detailed skill gap analysis with learning recommendations.

**Response:**
```json
{
  "application_id": 1,
  "skill_gap_analysis": {
    "summary": {
      "total_required_skills": 20,
      "skills_matched": 17,
      "skills_missing": 3,
      "gap_percentage": 15.0,
      "severity": "Low - Minor skills gap",
      "is_closeable": true
    },
    "gap_breakdown": {
      "critical_missing": {
        "count": 1,
        "skills": ["Kubernetes"],
        "impact": "High - Essential for role performance"
      },
      "important_missing": {
        "count": 2,
        "skills": ["AWS", "Docker"],
        "impact": "Medium - Important but can be learned on job"
      }
    },
    "learning_roadmap": [
      {
        "priority": 1,
        "skill": "Kubernetes",
        "difficulty": "intermediate",
        "estimated_weeks": 8,
        "learning_resources": [
          "Online courses for Kubernetes",
          "Official Kubernetes documentation"
        ]
      }
    ],
    "estimated_closure_time": {
      "total_weeks": 12,
      "total_months": 3.0,
      "skills_count": 3
    },
    "recommendations": [
      "PRIORITY: Focus on learning critical skills: Kubernetes",
      "Consider bootcamps, online courses, or certification programs"
    ]
  }
}
```

---

### 3. Get Skill Evidence Graph
**Endpoint:** `GET /analytics/application/{application_id}/skill-graph`

**Description:** Get graph data structure for skill visualization.

**Response:**
```json
{
  "application_id": 1,
  "skill_evidence_graph": {
    "graph": {
      "nodes": [
        {
          "id": "job",
          "label": "Job Requirements",
          "type": "job",
          "size": 30,
          "color": "#3498db"
        },
        {
          "id": "matched_1",
          "label": "Python",
          "type": "matched",
          "size": 20,
          "color": "#27ae60"
        }
      ],
      "edges": [
        {
          "source": "job",
          "target": "matched_1",
          "type": "required",
          "strength": 1.0,
          "color": "#27ae60",
          "label": "Matched"
        }
      ]
    },
    "statistics": {
      "total_nodes": 25,
      "total_edges": 40,
      "matched_skills_count": 17,
      "missing_skills_count": 3,
      "match_rate": 85.0
    },
    "legend": {
      "green": "Skills that match job requirements",
      "red": "Skills missing from candidate profile",
      "purple": "Additional skills candidate possesses"
    }
  }
}
```

---

### 4. Get Job Application Rankings
**Endpoint:** `GET /analytics/job/{job_id}/rankings`

**Query Parameters:**
- `limit` (optional): Maximum number of results (default: 100)

**Description:** Get ranked list of all applications for a job.

**Response:**
```json
{
  "job": {
    "id": 1,
    "role": "Senior Software Engineer",
    "company_id": 1
  },
  "total_applications": 50,
  "rankings": [
    {
      "rank": 1,
      "application_id": 101,
      "candidate": {
        "id": 25,
        "name": "John Doe",
        "email": "john@example.com",
        "experience": 6
      },
      "scores": {
        "composite_score": 0.92,
        "rfs": 0.90,
        "dcs": 0.95,
        "elc": 0.88
      },
      "decision": "Fast-Track Selected",
      "fraud_flag": false
    }
  ]
}
```

---

### 5. Get Top Candidates
**Endpoint:** `GET /analytics/job/{job_id}/top-candidates`

**Query Parameters:**
- `top_n` (optional): Number of top candidates to return (default: 10)

**Description:** Get top N candidates for recruiter quick view.

**Response:**
```json
{
  "job": {
    "id": 1,
    "role": "Senior Software Engineer"
  },
  "top_n": 10,
  "top_candidates": [
    {
      "rank": 1,
      "application_id": 101,
      "candidate": {
        "id": 25,
        "name": "John Doe",
        "email": "john@example.com",
        "mobile": "+1234567890",
        "experience": 6,
        "linkedin": "linkedin.com/in/johndoe",
        "github": "github.com/johndoe"
      },
      "scores": {
        "composite_score": 0.92,
        "match_percentage": "92.0%"
      },
      "skill_match_summary": {
        "matched_skills_count": 18,
        "missing_skills_count": 2,
        "match_score": 0.90
      },
      "decision": "Fast-Track Selected"
    }
  ]
}
```

---

### 6. Get Job Statistics
**Endpoint:** `GET /analytics/job/{job_id}/statistics`

**Description:** Get comprehensive statistics for a job's applications.

**Response:**
```json
{
  "job": {
    "id": 1,
    "role": "Senior Software Engineer"
  },
  "total_applications": 50,
  "decision_breakdown": {
    "Fast-Track Selected": 5,
    "Selected": 15,
    "Hire-Pooled": 20,
    "Rejected": 8,
    "Review Required": 2
  },
  "average_scores": {
    "composite": 0.65,
    "rfs": 0.68,
    "dcs": 0.62,
    "elc": 0.70
  },
  "fraud_statistics": {
    "total_fraud": 3,
    "fraud_percentage": 6.0
  },
  "top_candidate": {
    "name": "John Doe",
    "rank": 1,
    "score": 0.92,
    "decision": "Fast-Track Selected"
  }
}
```

---

### 7. Get Candidate Applications
**Endpoint:** `GET /analytics/candidate/{candidate_id}/applications`

**Description:** Get all applications submitted by a candidate (for candidate portal).

**Response:**
```json
{
  "candidate": {
    "id": 25,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "total_applications": 3,
  "applications": [
    {
      "application_id": 101,
      "job": {
        "id": 1,
        "role": "Senior Software Engineer",
        "company_name": "Tech Corp"
      },
      "rank": 1,
      "scores": {
        "composite_score": 0.92,
        "percentage": "92.0%"
      },
      "decision": "Selected",
      "status": "evaluated",
      "applied_at": "2026-02-12T10:30:00"
    }
  ]
}
```

---

## Database Migration

Before using these features, run the migration:

```bash
cd backend
python add_ranking_column.py
```

This adds the `rank` column to the `applications` table.

---

## Frontend Integration Examples

### 1. Display XAI Explanation (React Example)
```javascript
const fetchXAI = async (applicationId) => {
  const response = await fetch(`/analytics/application/${applicationId}/xai`);
  const data = await response.json();
  
  return data.xai_explanation;
};
```

### 2. Render Skill Evidence Graph (D3.js)
```javascript
const renderSkillGraph = async (applicationId) => {
  const response = await fetch(`/analytics/application/${applicationId}/skill-graph`);
  const data = await response.json();
  
  const graph = data.skill_evidence_graph.graph;
  
  // Use D3.js or any graph library to render nodes and edges
  // Green nodes = matched skills
  // Red nodes = missing skills
  // Purple nodes = extra skills
};
```

### 3. Show Top Candidates Dashboard
```javascript
const TopCandidates = ({ jobId }) => {
  const [candidates, setCandidates] = useState([]);
  
  useEffect(() => {
    fetch(`/analytics/job/${jobId}/top-candidates?top_n=10`)
      .then(res => res.json())
      .then(data => setCandidates(data.top_candidates));
  }, [jobId]);
  
  return (
    <div>
      {candidates.map(candidate => (
        <CandidateCard 
          key={candidate.application_id}
          rank={candidate.rank}
          name={candidate.candidate.name}
          score={candidate.scores.match_percentage}
        />
      ))}
    </div>
  );
};
```

---

## Key Benefits

1. **Transparency**: XAI provides clear explanations for every decision
2. **Fairness**: Candidates understand why they were selected/rejected
3. **Learning**: Skill gap analysis helps candidates improve
4. **Efficiency**: Rankings help recruiters focus on top candidates
5. **Visualization**: Skill graphs make comparisons intuitive
