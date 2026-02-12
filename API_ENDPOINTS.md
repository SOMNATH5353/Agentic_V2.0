# Agentic AI Hiring Platform - API Endpoints Documentation

## Base URL
```
https://agentic-v2-0.onrender.com
```

## Interactive Documentation
- **Swagger UI**: https://agentic-v2-0.onrender.com/docs
- **ReDoc**: https://agentic-v2-0.onrender.com/redoc

---

## 1. Root & Health Endpoints

### 1.1 Welcome Endpoint
**Method**: `GET`  
**Endpoint**: `/`  
**Description**: API information and available endpoints

**Input**: None

**Output**:
```json
{
  "message": "Welcome to Agentic AI Hiring Platform API",
  "version": "2.0",
  "features": ["AI-powered resume evaluation", "..."],
  "endpoints": {
    "documentation": "/docs",
    "health": "/health",
    "companies": "/company",
    "jobs": "/job",
    "applications": "/apply",
    "candidates": "/candidate",
    "analytics": "/analytics"
  }
}
```

### 1.2 Health Check
**Method**: `GET`  
**Endpoint**: `/health`  
**Description**: Service health status

**Input**: None

**Output**:
```json
{
  "status": "healthy",
  "service": "Agentic AI Hiring Platform",
  "version": "2.0.0"
}
```

---

## 2. Company Endpoints

### 2.1 Create Company
**Method**: `POST`  
**Endpoint**: `/company/`  
**Description**: Register a new company

**Input** (Form Data):
```
name: string (required)
description: string (required)
```

**Output**:
```json
{
  "id": 1,
  "name": "TechCorp",
  "description": "Leading technology company",
  "created_at": "2026-02-12T10:00:00"
}
```

---

## 3. Job Endpoints

### 3.1 Create Job with Company (Merged Endpoint) ⭐ RECOMMENDED
**Method**: `POST`  
**Endpoint**: `/job/create-with-company`  
**Description**: Create company and job posting in a single API call. If company exists, reuses it.

**Input** (Multipart Form):
```
# Company Details
company_name: string (required)
company_description: string (required)

# Job Details
role: string (required)
location: string (optional, default: "")
salary: string (optional, default: "")
employment_type: string (optional, default: "Full-time")
required_experience: integer (required)
jd_pdf: file (required, .pdf only)
```

**Output**:
```json
{
  "company": {
    "id": 1,
    "name": "TechCorp",
    "description": "Leading technology company",
    "created_at": "2026-02-12T10:00:00",
    "status": "created"
  },
  "job": {
    "id": 1,
    "company_id": 1,
    "role": "Python Developer",
    "location": "Remote",
    "salary": "$80k-$120k",
    "employment_type": "Full-time",
    "required_experience": 0,
    "created_at": "2026-02-12T10:00:00",
    "jd_text_preview": "We are looking for...",
    "embedding_dimensions": 768,
    "skills_stored": 15
  },
  "message": "Company created and job created successfully",
  "pages_parsed": 2,
  "skills_extracted": ["python", "flask", "rest api", "..."],
  "technical_skills": ["python", "flask", "sql", "git", "docker"],
  "soft_skills": ["communication", "teamwork", "problem solving"]
}
```

**Python Example**:
```python
import requests

with open("job_description.pdf", "rb") as f:
    response = requests.post(
        "https://agentic-v2-0.onrender.com/job/create-with-company",
        data={
            "company_name": "TechCorp",
            "company_description": "Leading technology company",
            "role": "Python Developer",
            "location": "Remote",
            "salary": "$80k-$120k",
            "employment_type": "Full-time",
            "required_experience": 0
        },
        files={"jd_pdf": f}
    )
print(response.json())
```

### 3.2 Create Job Posting (Separate)
**Method**: `POST`  
**Endpoint**: `/job/`  
**Description**: Create a new job by uploading JD PDF (requires existing company_id)

**Input** (Multipart Form):
```
company_id: integer (required)
role: string (required)
location: string (optional, default: "")
salary: string (optional, default: "")
employment_type: string (optional, default: "Full-time")
required_experience: integer (required)
jd_pdf: file (required, .pdf only)
```

**Output**:
```json
{
  "job": {
    "id": 1,
    "company_id": 1,
    "role": "Python Developer",
    "location": "Remote",
    "salary": "$80k-$120k",
    "employment_type": "Full-time",
    "required_experience": 0,
    "created_at": "2026-02-12T10:00:00",
    "jd_text_preview": "We are looking for...",
    "embedding_dimensions": 768,
    "skills_stored": 15
  },
  "message": "Job created and stored in database successfully",
  "pages_parsed": 2,
  "skills_extracted": ["python", "flask", "rest api", "..."],
  "technical_skills": ["python", "flask", "sql", "git", "docker"],
  "soft_skills": ["communication", "teamwork", "problem solving"]
}
```

### 3.3 Get Job Details
**Method**: `GET`  
**Endpoint**: `/job/{job_id}`  
**Description**: Get detailed job information

**Input** (Path Parameter):
```
job_id: integer (required)
```

**Output**:
```json
{
  "id": 1,
  "company_id": 1,
  "company_name": "TechCorp",
  "company_description": "Leading technology company",
  "role": "Python Developer",
  "location": "Remote",
  "salary": "$80k-$120k",
  "employment_type": "Full-time",
  "required_experience": 0,
  "jd_text": "Full job description text...",
  "created_at": "2026-02-12T10:00:00",
  "application_count": 25,
  "skills_required": ["python", "flask", "rest api", "..."],
  "technical_skills": ["python", "flask", "sql"],
  "soft_skills": ["communication", "teamwork"]
}
```

### 3.4 List Jobs
**Method**: `GET`  
**Endpoint**: `/job/`  
**Description**: Browse available jobs with filters

**Input** (Query Parameters):
```
company_id: integer (optional)
location: string (optional)
employment_type: string (optional)
skip: integer (optional, default: 0)
limit: integer (optional, default: 100)
```

**Output**:
```json
{
  "total": 50,
  "showing": 10,
  "skip": 0,
  "limit": 100,
  "jobs": [
    {
      "id": 1,
      "role": "Python Developer",
      "company_id": 1,
      "company_name": "TechCorp",
      "location": "Remote",
      "salary": "$80k-$120k",
      "employment_type": "Full-time",
      "required_experience": 0,
      "created_at": "2026-02-12T10:00:00",
      "application_count": 25,
      "skills_preview": ["python", "flask", "sql", "git", "docker"]
    }
  ]
}
```

### 3.5 Get Company Applications
**Method**: `GET`  
**Endpoint**: `/job/{company_id}/applications`  
**Description**: Get all applications across all jobs for a specific company

**Input**:
```
Path: company_id: integer (required)
Query: status_filter: string (optional)
```

**Output**:
```json
{
  "company": {
    "id": 1,
    "name": "TechCorp"
  },
  "total_applications": 25,
  "total_jobs": 3,
  "statistics": {
    "fast_track": 5,
    "selected": 8,
    "hire_pooled": 7,
    "rejected": 4,
    "review_required": 1
  },
  "applications": [...]
}
```

---

## 4. Application Endpoints

### 4.1 Submit Application
**Method**: `POST`  
**Endpoint**: `/apply/{company_id}`  
**Description**: Submit job application with resume PDF

**Input**:
```
Path: company_id: integer (required)

Multipart Form:
job_id: integer (required) - Must belong to the specified company
name: string (required)
email: string (required)
mobile: string (required)
linkedin: string (optional)
github: string (optional)
experience: integer (required)
resume_pdf: file (required, .pdf only)
```

**Output**:
```json
{
  "application_id": 101,
  "candidate_id": 42,
  "job_id": 1,
  "decision": "Selected",
  "composite_score": 0.78,
  "explanation": {
    "basic_explanation": {...},
    "xai_explanation": {...},
    "skill_gap_analysis": {...},
    "skill_evidence_graph": {...}
  },
  "message": "Application evaluated successfully",
  "pages_parsed": 2,
  "skills_detected": 12
}
```

**Python Example**:
```python
import requests

with open("resume.pdf", "rb") as f:
    response = requests.post(
        "https://agentic-v2-0.onrender.com/apply/1",  # company_id = 1
        data={
            "job_id": 5,  # Must belong to company 1
            "name": "Arjun Malhotra",
            "email": "arjun@example.com",
            "mobile": "1234567890",
            "experience": 2
        },
        files={"resume_pdf": f}
    )
print(response.json())
```

### 4.2 Get Application Details
**Method**: `GET`  
**Endpoint**: `/apply/{application_id}`  
**Description**: Get complete application details

**Input** (Path Parameter):
```
application_id: integer (required)
```

**Output**:
```json
{
  "application": {
    "id": 101,
    "job_id": 1,
    "candidate_id": 42,
    "rfs": 0.85,
    "dcs": 0.75,
    "elc": 1.0,
    "composite_score": 0.78,
    "rank": 3,
    "decision": "Selected",
    "fraud_flag": false,
    "created_at": "2026-02-12T10:00:00"
  },
  "candidate": {
    "id": 42,
    "name": "Arjun Malhotra",
    "email": "arjun@example.com",
    "mobile": "1234567890",
    "experience": 2
  },
  "job": {
    "id": 1,
    "role": "Python Developer",
    "company_name": "TechCorp"
  },
  "explanation": {...}
}
```

### 4.3 Get Application History
**Method**: `GET`  
**Endpoint**: `/apply/{application_id}/history`  
**Description**: Get audit trail for application

**Input** (Path Parameter):
```
application_id: integer (required)
```

**Output**:
```json
{
  "application_id": 101,
  "total_events": 5,
  "history": [
    {
      "timestamp": "2026-02-12T10:00:00",
      "event_type": "application_created",
      "details": {...}
    }
  ]
}
```

### 4.4 List Applications
**Method**: `GET`  
**Endpoint**: `/apply/`  
**Description**: List all applications with filters

**Input** (Query Parameters):
```
decision: string (optional)
fraud_flag: boolean (optional)
skip: integer (optional, default: 0)
limit: integer (optional, default: 100)
```

**Output**:
```json
{
  "total": 150,
  "showing": 100,
  "skip": 0,
  "limit": 100,
  "applications": [...]
}
```

---

## 5. Candidate Endpoints

### 5.1 Get Candidate Details
**Method**: `GET`  
**Endpoint**: `/candidate/{candidate_id}`  
**Description**: Get candidate information

**Input** (Path Parameter):
```
candidate_id: integer (required)
```

**Output**:
```json
{
  "id": 42,
  "name": "Arjun Malhotra",
  "email": "arjun@example.com",
  "mobile": "1234567890",
  "linkedin": "linkedin.com/in/arjun",
  "github": "github.com/arjun",
  "experience": 2,
  "created_at": "2026-02-12T10:00:00",
  "skills_extracted": {
    "all_skills": ["python", "flask", "sql", "..."],
    "technical_skills": ["python", "flask", "sql"],
    "soft_skills": ["communication", "teamwork"]
  }
}
```

### 5.2 Get Candidate Applications
**Method**: `GET`  
**Endpoint**: `/candidate/{candidate_id}/applications`  
**Description**: Get all applications by candidate

**Input** (Path Parameter):
```
candidate_id: integer (required)
```

**Output**:
```json
{
  "candidate": {
    "id": 42,
    "name": "Arjun Malhotra",
    "email": "arjun@example.com"
  },
  "total_applications": 3,
  "applications": [...]
}
```

### 5.3 Get Candidate History
**Method**: `GET`  
**Endpoint**: `/candidate/{candidate_id}/history`  
**Description**: Get audit trail for candidate

**Input** (Path Parameter):
```
candidate_id: integer (required)
```

**Output**:
```json
{
  "candidate_id": 42,
  "total_events": 8,
  "history": [...]
}
```

### 5.4 Search Candidate by Email
**Method**: `GET`  
**Endpoint**: `/candidate/search/by-email`  
**Description**: Find candidate by email address

**Input** (Query Parameter):
```
email: string (required)
```

**Output**: Same as Get Candidate Details

### 5.5 List All Candidates
**Method**: `GET`  
**Endpoint**: `/candidate/`  
**Description**: List all candidates with pagination

**Input** (Query Parameters):
```
skip: integer (optional, default: 0)
limit: integer (optional, default: 100)
```

**Output**:
```json
{
  "total": 200,
  "showing": 100,
  "skip": 0,
  "limit": 100,
  "candidates": [...]
}
```

---

## 6. Analytics Endpoints

### 6.1 Get XAI Explanation
**Method**: `GET`  
**Endpoint**: `/analytics/application/{application_id}/xai`  
**Description**: Get explainable AI explanation for application

**Input** (Path Parameter):
```
application_id: integer (required)
```

**Output**:
```json
{
  "application_id": 101,
  "candidate": {
    "name": "Arjun Malhotra",
    "experience": 2
  },
  "job": {
    "role": "Python Developer",
    "required_experience": 0
  },
  "xai_explanation": {
    "decision": "Selected",
    "confidence_level": {
      "level": "high",
      "score": 0.85,
      "explanation": "Decision confidence based on score clarity"
    },
    "key_factors": [
      {
        "factor": "Skill Match",
        "impact": "High",
        "value": "75%",
        "contribution": "+25 points"
      }
    ],
    "strengths": ["Strong Python skills", "Flask experience", "..."],
    "areas_for_improvement": ["Learn Docker", "AWS certification", "..."],
    "score_breakdown": {
      "rfs": 0.85,
      "dcs": 0.75,
      "elc": 1.0,
      "composite": 0.78
    },
    "decision_rationale": "Candidate shows strong...",
    "recommendations": ["Consider for interview", "..."]
  }
}
```

### 6.2 Get Skill Gap Analysis
**Method**: `GET`  
**Endpoint**: `/analytics/application/{application_id}/skill-gap`  
**Description**: Get detailed skill gap analysis

**Input** (Path Parameter):
```
application_id: integer (required)
```

**Output**:
```json
{
  "application_id": 101,
  "candidate": {
    "name": "Arjun Malhotra",
    "email": "arjun@example.com"
  },
  "job": {
    "role": "Python Developer"
  },
  "skill_gap_analysis": {
    "summary": {
      "total_required_skills": 20,
      "skills_matched": 12,
      "skills_missing": 8,
      "skills_missing_required": 2,
      "skills_missing_nice_to_have": 6,
      "gap_percentage": 40.0,
      "gap_percentage_required": 14.29,
      "severity": "Medium - Moderate skills gap",
      "is_closeable": true,
      "focus_on_required": true
    },
    "gap_breakdown": {
      "critical_missing": {
        "count": 1,
        "skills": ["kubernetes"],
        "impact": "High - Essential for role performance (Required Skills)"
      },
      "important_missing": {
        "count": 1,
        "skills": ["docker"],
        "impact": "Medium - Important but can be learned on job (Required Skills)"
      },
      "nice_to_have_missing": {
        "count": 6,
        "skills": ["aws", "azure", "terraform", "..."],
        "impact": "Low - Beneficial but not critical (Nice-to-Have Skills)"
      }
    },
    "transferable_skills": {
      "count": 2,
      "skills": [
        {
          "from_skill": "python",
          "to_skill": "java",
          "transfer_ease": "Easy - Related technology"
        }
      ]
    },
    "learning_roadmap": [
      {
        "priority": 1,
        "skill": "kubernetes",
        "difficulty": "intermediate",
        "estimated_weeks": 8,
        "learning_resources": [
          "Online courses for kubernetes",
          "Official kubernetes documentation"
        ]
      }
    ],
    "estimated_closure_time": {
      "total_weeks": 34,
      "total_months": 8.4,
      "skills_count": 8
    },
    "recommendations": [
      "PRIORITY: Focus on learning critical skills: kubernetes",
      "Next, work on important skills: docker",
      "Optional: Add value with: aws, azure"
    ]
  }
}
```

### 6.3 Get Skill Evidence Graph
**Method**: `GET`  
**Endpoint**: `/analytics/application/{application_id}/skill-graph`  
**Description**: Get graph data for skill visualization

**Input** (Path Parameter):
```
application_id: integer (required)
```

**Output**:
```json
{
  "application_id": 101,
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
          "label": "python",
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
      "total_edges": 35,
      "matched_skills_count": 12,
      "missing_skills_count": 8,
      "extra_skills_count": 5,
      "match_rate": 60.0
    },
    "legend": {
      "green": "Skills that match job requirements",
      "red": "Skills missing from candidate profile",
      "purple": "Additional skills candidate possesses"
    },
    "visualization_config": {
      "layout": "force-directed",
      "show_labels": true,
      "interactive": true,
      "zoom_enabled": true
    }
  }
}
```

### 6.4 Get Job Application Rankings
**Method**: `GET`  
**Endpoint**: `/analytics/job/{job_id}/rankings`  
**Description**: Get ranked list of all applications

**Input**:
```
Path: job_id: integer (required)
Query: limit: integer (optional, default: 100)
```

**Output**:
```json
{
  "job": {
    "id": 1,
    "role": "Python Developer",
    "company_id": 1
  },
  "total_applications": 25,
  "rankings": [
    {
      "rank": 1,
      "application_id": 101,
      "candidate": {
        "id": 42,
        "name": "Arjun Malhotra",
        "email": "arjun@example.com",
        "experience": 2
      },
      "scores": {
        "composite_score": 0.89,
        "rfs": 0.90,
        "dcs": 0.85,
        "elc": 1.0
      },
      "decision": "Fast-Track Selected",
      "fraud_flag": false,
      "created_at": "2026-02-12T10:00:00"
    }
  ]
}
```

### 6.5 Get Top N Candidates
**Method**: `GET`  
**Endpoint**: `/analytics/job/{job_id}/top-candidates`  
**Description**: Get top candidates for recruiter dashboard

**Input**:
```
Path: job_id: integer (required)
Query: top_n: integer (optional, default: 10)
```

**Output**:
```json
{
  "job": {
    "id": 1,
    "role": "Python Developer",
    "company_id": 1
  },
  "top_n": 10,
  "top_candidates": [
    {
      "rank": 1,
      "application_id": 101,
      "candidate": {
        "id": 42,
        "name": "Arjun Malhotra",
        "email": "arjun@example.com",
        "mobile": "1234567890",
        "experience": 2,
        "linkedin": "linkedin.com/in/arjun",
        "github": "github.com/arjun"
      },
      "scores": {
        "composite_score": 0.89,
        "match_percentage": "89.0%"
      },
      "skill_match_summary": {
        "matched_skills_count": 15,
        "missing_skills_count": 3,
        "match_score": 0.85
      },
      "decision": "Fast-Track Selected",
      "created_at": "2026-02-12T10:00:00"
    }
  ]
}
```

### 6.6 Get Job Statistics
**Method**: `GET`  
**Endpoint**: `/analytics/job/{job_id}/statistics`  
**Description**: Get comprehensive job application statistics

**Input** (Path Parameter):
```
job_id: integer (required)
```

**Output**:
```json
{
  "job": {
    "id": 1,
    "role": "Python Developer",
    "company_id": 1
  },
  "total_applications": 25,
  "decision_breakdown": {
    "Fast-Track Selected": 5,
    "Selected": 8,
    "Hire-Pooled": 7,
    "Rejected": 4,
    "Review Required": 1
  },
  "average_scores": {
    "composite": 0.6543,
    "rfs": 0.7021,
    "dcs": 0.6234,
    "elc": 0.7891
  },
  "fraud_statistics": {
    "total_fraud": 2,
    "fraud_percentage": 8.0
  },
  "top_candidate": {
    "name": "Arjun Malhotra",
    "rank": 1,
    "score": 0.89,
    "decision": "Fast-Track Selected"
  }
}
```

### 6.7 Get Candidate Applications (Analytics)
**Method**: `GET`  
**Endpoint**: `/analytics/candidate/{candidate_id}/applications`  
**Description**: Get all applications by candidate (for candidate portal)

**Input** (Path Parameter):
```
candidate_id: integer (required)
```

**Output**:
```json
{
  "candidate": {
    "id": 42,
    "name": "Arjun Malhotra",
    "email": "arjun@example.com"
  },
  "total_applications": 3,
  "applications": [
    {
      "application_id": 101,
      "job": {
        "id": 1,
        "role": "Python Developer",
        "company_name": "TechCorp"
      },
      "rank": 1,
      "scores": {
        "composite_score": 0.89,
        "percentage": "89.0%"
      },
      "decision": "Fast-Track Selected",
      "status": "evaluated",
      "applied_at": "2026-02-12T10:00:00"
    }
  ]
}
```

---

## Summary by Category

### Total Endpoints: 29

| Category | Count | Endpoints |
|----------|-------|-----------|
| Root & Health | 2 | `/`, `/health` |
| Company | 1 | `POST /company/` |
| Job | 5 | `POST /job/create-with-company` ⭐, `POST /job/`, `GET /job/{id}`, `GET /job/`, `GET /job/{company_id}/applications` |
| Application | 4 | `POST /apply/{company_id}`, `GET /apply/{id}`, `GET /apply/{id}/history`, `GET /apply/` |
| Candidate | 5 | `GET /candidate/{id}`, `GET /candidate/{id}/applications`, `GET /candidate/{id}/history`, `GET /candidate/search/by-email`, `GET /candidate/` |
| Analytics | 7 | XAI, Skill Gap, Skill Graph, Rankings, Top Candidates, Statistics, Candidate Applications |

---

## Common Response Codes

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Successful GET request |
| 201 | Created | Successful POST request |
| 400 | Bad Request | Invalid input (e.g., non-PDF file) |
| 404 | Not Found | Resource doesn't exist |
| 422 | Validation Error | Missing required parameters |
| 500 | Server Error | Internal error |

---

## Key Features

1. **Resume Parsing**: Automatic PDF parsing and text extraction
2. **Skill Extraction**: NLP-based technical and soft skill detection
3. **AI Evaluation**: Multi-score evaluation (RFS, DCS, ELC, Composite)
4. **Fraud Detection**: Duplicate resume and email detection
5. **XAI Explainability**: Transparent decision explanations
6. **Skill Gap Analysis**: Learning roadmaps and recommendations
7. **Ranking System**: Automatic candidate ranking per job
8. **Analytics Dashboard**: Comprehensive statistics and insights
9. **Audit Trail**: Complete history logging
10. **Filtering**: Advanced filtering on jobs and applications

---

## Authentication

Currently: **None** (Open API)  
**Note**: In production, add authentication middleware (JWT, OAuth2, etc.)

---

## Rate Limiting

Currently: **None**  
**Recommended**: Implement rate limiting for production (e.g., 100 requests/minute)

---

## Testing the API

1. **Using Swagger UI**: Visit https://agentic-v2-0.onrender.com/docs
2. **Using cURL**: See example commands in each endpoint section
3. **Using Postman**: Import OpenAPI spec from `/openapi.json`
4. **Using Python requests**:

```python
import requests

# Create company
response = requests.post(
    "https://agentic-v2-0.onrender.com/company/",
    params={"name": "TechCorp", "description": "Tech company"}
)
print(response.json())

# Create job
with open("job_description.pdf", "rb") as f:
    response = requests.post(
        "https://agentic-v2-0.onrender.com/job/",
        data={
            "company_id": 1,
            "role": "Python Developer",
            "location": "Remote",
            "salary": "$80k-$120k",
            "employment_type": "Full-time",
            "required_experience": 0
        },
        files={"jd_pdf": f}
    )
print(response.json())

# Apply for job
with open("resume.pdf", "rb") as f:
    response = requests.post(
        "https://agentic-v2-0.onrender.com/apply/1",
        data={
            "name": "Arjun Malhotra",
            "email": "arjun@example.com",
            "mobile": "1234567890",
            "experience": 2
        },
        files={"resume_pdf": f}
    )
print(response.json())
```

---

## Contact & Support

For issues or questions, refer to the project README or contact the development team.
