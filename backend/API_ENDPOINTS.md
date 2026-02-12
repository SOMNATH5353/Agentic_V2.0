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
