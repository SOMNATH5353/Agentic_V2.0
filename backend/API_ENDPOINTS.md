# API Endpoints for Job Application System

## For Recruiters - Job Posting Dashboard

### 1. Create a New Job Posting
**Endpoint:** `POST /job/`

**Form Data:**
- `company_id` (int, required): Company ID
- `role` (string, required): Job title/role (e.g., "Senior Software Engineer")
- `location` (string, optional): Job location (e.g., "New York, NY" or "Remote")
- `salary` (string, optional): Salary range (e.g., "$100k-150k")
- `employment_type` (string, optional): "Full-time", "Part-time", "Contract", "Internship" (default: "Full-time")
- `required_experience` (int, required): Years of experience required
- `jd_pdf` (file, required): Job description PDF file

**Example Response:**
```json
{
  "job": {
    "id": 1,
    "company_id": 1,
    "role": "Senior Software Engineer",
    "location": "San Francisco, CA",
    "salary": "$120k-180k",
    "employment_type": "Full-time",
    "required_experience": 5,
    "created_at": "2026-02-12T10:30:00",
    "skills_stored": 25
  },
  "message": "Job created and stored in database successfully"
}
```

### 2. View Applications for a Job
**Endpoint:** `GET /job/{job_id}/applications`

**Query Parameters:**
- `status_filter` (optional): Filter by decision status

**Example Response:**
```json
{
  "job": {
    "id": 1,
    "role": "Senior Software Engineer",
    "company_id": 1
  },
  "total_applications": 50,
  "statistics": {
    "fast_track": 5,
    "selected": 15,
    "hire_pooled": 20,
    "rejected": 10
  },
  "applications": [...]
}
```

---

## For Candidates - Job Browsing & Application

### 1. Browse All Available Jobs
**Endpoint:** `GET /job/`

**Query Parameters:**
- `company_id` (optional): Filter by company
- `location` (optional): Filter by location (partial match)
- `employment_type` (optional): Filter by employment type
- `skip` (optional): Pagination offset (default: 0)
- `limit` (optional): Results per page (default: 100)

**Example Response:**
```json
{
  "total": 25,
  "showing": 10,
  "skip": 0,
  "limit": 10,
  "jobs": [
    {
      "id": 1,
      "role": "Senior Software Engineer",
      "company_id": 1,
      "company_name": "Tech Corp",
      "location": "San Francisco, CA",
      "salary": "$120k-180k",
      "employment_type": "Full-time",
      "required_experience": 5,
      "created_at": "2026-02-12T10:30:00",
      "application_count": 50,
      "skills_preview": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"]
    }
  ]
}
```

### 2. View Job Details
**Endpoint:** `GET /job/{job_id}`

**Example Response:**
```json
{
  "id": 1,
  "company_id": 1,
  "company_name": "Tech Corp",
  "company_description": "Leading technology company...",
  "role": "Senior Software Engineer",
  "location": "San Francisco, CA",
  "salary": "$120k-180k",
  "employment_type": "Full-time",
  "required_experience": 5,
  "jd_text": "Full job description text...",
  "created_at": "2026-02-12T10:30:00",
  "application_count": 50,
  "skills_required": ["Python", "FastAPI", "PostgreSQL", ...],
  "technical_skills": ["Python", "FastAPI", "Docker"],
  "soft_skills": ["Communication", "Leadership"]
}
```

### 3. Apply to a Job
**Endpoint:** `POST /apply/{job_id}`

**Form Data:**
- `name` (string, required): Full name
- `email` (string, required): Email address
- `mobile` (string, required): Mobile/phone number
- `linkedin` (string, optional): LinkedIn profile URL
- `github` (string, optional): GitHub profile URL
- `experience` (int, required): Years of experience
- `resume_pdf` (file, required): Resume PDF file

**Example Response:**
```json
{
  "application_id": 101,
  "candidate_id": 50,
  "job_id": 1,
  "decision": "Selected",
  "scores": {
    "skills_match": 85.5,
    "experience_match": 90.0,
    "overall_score": 87.8
  },
  "message": "Application submitted successfully"
}
```

---

## Frontend Implementation Guide

### Job Listing Page (For Candidates)

1. **Fetch all jobs**: `GET /job/`
2. **Display job cards** with:
   - Company name
   - Job title
   - Location
   - Salary
   - Employment type
   - Experience required
   - Number of applicants
   - "Apply Now" button

3. **Click on job card**: Navigate to job detail page

### Job Detail Page

1. **Fetch job details**: `GET /job/{job_id}`
2. **Display full information**:
   - All job fields
   - Full job description
   - Required skills
   - Company information
   
3. **Apply button**: Opens application form modal

### Application Form

1. **Form fields**:
   - Name (text input)
   - Email (email input)
   - Mobile (tel input)
   - LinkedIn (url input, optional)
   - GitHub (url input, optional)
   - Experience (number input)
   - Resume (file input, accept=".pdf")

2. **On submit**: 
   - `POST /apply/{job_id}` with form data
   - Show success message with application ID and decision
   - Redirect to application status page

### Recruiter Dashboard

1. **Job Creation Form**:
   - Company selection (dropdown)
   - Job title (text input)
   - Location (text input)
   - Salary (text input)
   - Employment type (dropdown: Full-time, Part-time, Contract, Internship)
   - Required experience (number input)
   - Job description (file input, accept=".pdf")

2. **Submit**: `POST /job/` with form data

3. **View Applications**: 
   - List all jobs for company
   - Click on job to see applications: `GET /job/{job_id}/applications`
   - Filter by status

---

## Database Migration

Before using the new features, run the migration script:

```bash
cd backend
python add_new_columns.py
```

This will add:
- `mobile` column to `candidates` table
- `location` column to `jobs` table
- `employment_type` column to `jobs` table

---

## Candidate Master Endpoint

### Get Complete Candidate Profile
**Endpoint:** `GET /candidate/{candidate_id}/master`

**Description:** 
This is a comprehensive master endpoint that returns all details about a candidate including:
- Complete personal information (name, email, mobile, LinkedIn, GitHub, experience)
- All skills extracted from resume
- Complete list of all job applications
- For each application:
  - Full job details (role, location, salary, job description, required skills)
  - Company information
  - All scores (Role Fit Score, Domain Competency Score, Experience Level Compatibility, Composite Score)
  - Ranking among all applicants
  - Decision status (Selected/Rejected/Pending)
  - Decision reasoning and detailed explanation
  - Fraud detection information
  - Skill match analysis
  - Application status

**Example Request:**
```
GET /candidate/1/master
```

**Example Response:**
```json
{
  "candidate_profile": {
    "candidate_id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "mobile": "+1234567890",
    "linkedin": "https://linkedin.com/in/johndoe",
    "github": "https://github.com/johndoe",
    "years_of_experience": 5,
    "skills": ["Python", "JavaScript", "React", "Node.js", "SQL"],
    "resume_text": "Full resume text...",
    "profile_created_at": "2026-01-15T10:00:00"
  },
  "application_summary": {
    "total_applications": 10,
    "selected": 3,
    "rejected": 5,
    "pending": 2,
    "average_composite_score": 78.5,
    "best_application": {
      "application_id": 5,
      "job_role": "Senior Python Developer",
      "composite_score": 92.3,
      "decision": "Selected",
      "rank": 1
    }
  },
  "applications": [
    {
      "application_id": 5,
      "applied_at": "2026-02-10T14:30:00",
      "status": "evaluated",
      "job_details": {
        "job_id": 10,
        "role": "Senior Python Developer",
        "location": "New York, NY",
        "salary": "$120k-150k",
        "employment_type": "Full-time",
        "required_experience": 5,
        "job_description": "We are looking for...",
        "required_skills": ["Python", "Django", "PostgreSQL", "Docker"]
      },
      "company_details": {
        "company_id": 2,
        "company_name": "Tech Corp Inc",
        "company_description": "Leading tech company..."
      },
      "scores": {
        "role_fit_score": 88.5,
        "domain_competency_score": 92.0,
        "experience_level_compatibility": 95.0,
        "composite_score": 92.3,
        "rank": 1,
        "rank_description": "Ranked #1"
      },
      "decision": {
        "status": "Selected",
        "reason": "Excellent match for the role with strong technical skills",
        "detailed_explanation": {
          "strengths": ["Strong Python expertise", "Relevant experience"],
          "concerns": []
        }
      },
      "fraud_detection": {
        "fraud_flag": false,
        "similarity_index": 0.15,
        "fraud_details": null
      },
      "skill_analysis": {
        "skill_match": {
          "matched_skills": ["Python", "PostgreSQL"],
          "missing_skills": ["Docker"]
        },
        "experience_details": {
          "years": 5,
          "relevance": "high"
        }
      }
    }
  ]
}
```

**Use Cases:**
- Complete candidate profile view for HR dashboard
- Candidate's application history tracking
- Performance analysis across multiple applications
- Export candidate data for reporting
- Comprehensive audit trail

---

## Candidate Master Endpoint - All Candidates

### Get Complete Details for All Candidates
**Endpoint:** `GET /candidate/master/all`

**Query Parameters:**
- `skip` (int, optional, default: 0): Number of candidates to skip for pagination
- `limit` (int, optional, default: 100, max: 500): Maximum number of candidates to return

**Description:**
This endpoint returns comprehensive details for ALL candidates in the system with pagination support. For each candidate, it includes the same detailed information as the single candidate master endpoint.

**Example Request:**
```
GET /candidate/master/all?skip=0&limit=50
```

**Example Response:**
```json
{
  "total_candidates": 250,
  "showing": 50,
  "skip": 0,
  "limit": 50,
  "global_statistics": {
    "total_applications": 523,
    "total_selected": 145,
    "total_rejected": 298,
    "total_pending": 80
  },
  "candidates": [
    {
      "candidate_profile": {
        "candidate_id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "mobile": "+1234567890",
        "linkedin": "https://linkedin.com/in/johndoe",
        "github": "https://github.com/johndoe",
        "years_of_experience": 5,
        "skills": ["Python", "JavaScript", "React", "Node.js"],
        "resume_text": "Full resume text...",
        "profile_created_at": "2026-01-15T10:00:00"
      },
      "application_summary": {
        "total_applications": 10,
        "selected": 3,
        "rejected": 5,
        "pending": 2,
        "average_composite_score": 78.5,
        "best_application": {
          "application_id": 5,
          "job_role": "Senior Python Developer",
          "composite_score": 92.3,
          "decision": "Selected",
          "rank": 1
        }
      },
      "applications": [
        {
          "application_id": 5,
          "applied_at": "2026-02-10T14:30:00",
          "status": "evaluated",
          "job_details": { },
          "company_details": { },
          "scores": { },
          "decision": { },
          "fraud_detection": { },
          "skill_analysis": { }
        }
      ]
    }
  ]
}
```

**Features:**
- Returns all candidates with complete details
- Pagination support (max 500 candidates per request)
- Global statistics showing totals across all candidates
- Each candidate includes full profile, applications, and analysis
- Efficient for bulk data export and system-wide reporting

**Use Cases:**
- Admin dashboard with complete candidate database
- Bulk export for HR analytics and reporting
- System-wide statistics and insights
- Candidate benchmarking and comparison
- Data migration and backup
- Mass processing and analysis

