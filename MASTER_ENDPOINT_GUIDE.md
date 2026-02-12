# Candidate Master Endpoints - Quick Reference

## Overview
Two comprehensive API endpoints have been created that return complete candidate information including all applications, scores, decisions, and detailed analysis:

1. **Single Candidate Master**: Get complete details for one specific candidate
2. **All Candidates Master**: Get complete details for all candidates with pagination

---

## Endpoint 1: Single Candidate Master

**URL:** `GET /candidate/{candidate_id}/master`

**Example:** `http://localhost:8000/candidate/1/master`

## What This Endpoint Returns

### 1. Candidate Profile
- **Personal Details**: Name, email, mobile, LinkedIn, GitHub
- **Experience**: Years of experience
- **Skills**: All skills extracted from resume
- **Resume**: Full resume text
- **Created Date**: When the profile was created

### 2. Application Summary
- **Total Applications**: Count of all applications
- **Selected**: Number of selected applications
- **Rejected**: Number of rejected applications  
- **Pending**: Number of pending applications
- **Average Score**: Average composite score across all applications
- **Best Application**: Highlights the highest-scoring application with:
  - Job role
  - Composite score
  - Decision status
  - Rank

### 3. Detailed Applications
For each application, the endpoint returns:

#### Job Information
- Job ID, role, location, salary
- Employment type (Full-time, Part-time, etc.)
- Required experience
- Full job description
- Required skills list

#### Company Information
- Company ID, name, and description

#### All Scores
- **RFS** (Role Fit Score)
- **DCS** (Domain Competency Score)
- **ELC** (Experience Level Compatibility)
- **Composite Score**
- **Rank** among all applicants

#### Decision Details
- Status (Selected/Rejected/Pending)
- Reason for decision
- Detailed explanation

#### Fraud Detection
- Fraud flag (true/false)
- Similarity index
- Fraud details (if any)

#### Skill Analysis
- Matched skills vs missing skills
- Experience compatibility details

---

## Endpoint 2: All Candidates Master

**URL:** `GET /candidate/master/all`

**Example:** `http://localhost:8000/candidate/master/all?skip=0&limit=10`

### What This Endpoint Returns

This endpoint returns the same comprehensive data as Endpoint 1, but for **all candidates** in the system with pagination support.

#### Response Structure
```json
{
  "total_candidates": 250,
  "showing": 10,
  "skip": 0,
  "limit": 10,
  "global_statistics": {
    "total_applications": 523,
    "total_selected": 145,
    "total_rejected": 298,
    "total_pending": 80
  },
  "candidates": [
    {
      "candidate_profile": { ... },
      "application_summary": { ... },
      "applications": [ ... ]
    }
  ]
}
```

#### Pagination Parameters
- **skip**: Number of candidates to skip (default: 0)
- **limit**: Maximum candidates to return (default: 100, max: 500)

#### Global Statistics
- Total applications across all candidates
- Total selected, rejected, and pending applications
- Aggregate data for system-wide insights

#### Per Candidate Data
Each candidate in the array includes:
- All the same details as the single candidate endpoint
- Complete profile, applications, scores, decisions
- Summary statistics specific to that candidate

---

## Testing the Endpoints

### Endpoint 1: Single Candidate Master

#### Option 1: Using the Test Script
```bash
python test_master_endpoint.py
```

This will:
- Prompt you for a candidate ID
- Fetch all data from the endpoint
- Display a formatted summary
- Save the full JSON response to a file

#### Option 2: Using cURL
```bash
curl http://localhost:8000/candidate/1/master
```

#### Option 3: Using Browser/Swagger
- Open: http://localhost:8000/docs
- Look for `/candidate/{candidate_id}/master` endpoint
- Click "Try it out"
- Enter a candidate ID
- Click "Execute"

### Endpoint 2: All Candidates Master

#### Option 1: Using the Test Script
```bash
python test_all_candidates_master.py
```

This will:
- Offer two options: quick view or complete export
- Allow you to specify pagination (skip/limit)
- Display formatted summary of all candidates
- Save the full JSON response to a file
- For export mode: automatically fetch all candidates in batches

#### Option 2: Using cURL
```bash
# Get first 10 candidates
curl "http://localhost:8000/candidate/master/all?limit=10"

# Get next 10 candidates
curl "http://localhost:8000/candidate/master/all?skip=10&limit=10"

# Get up to 100 candidates
curl "http://localhost:8000/candidate/master/all?limit=100"
```

#### Option 3: Using Browser/Swagger
- Open: http://localhost:8000/docs
- Look for `/candidate/master/all` endpoint
- Click "Try it out"
- Enter skip and limit values
- Click "Execute"

## Files Modified/Created

1. **backend/app/routes/candidate_routes.py**
   - Added single candidate master endpoint (`/{candidate_id}/master`)
   - Added all candidates master endpoint (`/master/all`)
   - Imports Company and Job models

2. **backend/API_ENDPOINTS.md**
   - Added documentation for both endpoints

3. **API_ENDPOINTS.md** (root)
   - Added comprehensive documentation with examples

4. **test_master_endpoint.py** (new)
   - Created test script for single candidate endpoint

5. **test_all_candidates_master.py** (new)
   - Created test script for all candidates endpoint
   - Includes pagination testing and complete export functionality

## Use Cases

### Single Candidate Endpoint
1. **HR Dashboard**: Display complete candidate profile with all history
2. **Performance Tracking**: Track candidate success across multiple applications
3. **Candidate Portal**: Show candidates their application history and status
4. **Individual Review**: Deep dive into specific candidate details

### All Candidates Endpoint
1. **Admin Dashboard**: System-wide view of all candidates
2. **Bulk Export**: Export all candidate data for external analytics
3. **Reporting**: Generate comprehensive reports across entire candidate database
4. **Benchmarking**: Compare candidates and identify top performers
5. **Audit Trail**: Complete system audit for compliance
6. **Data Migration**: Backup and transfer complete candidate database

## Example Response Structures

### Single Candidate Endpoint Response
```json
{
  "candidate_profile": {
    "candidate_id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    ...
  },
  "application_summary": {
    "total_applications": 10,
    "selected": 3,
    "rejected": 5,
    "pending": 2,
    "average_composite_score": 78.5,
    "best_application": { ... }
  },
  "applications": [
    {
      "application_id": 101,
      "job_details": { ... },
      "company_details": { ... },
      "scores": { ... },
      "decision": { ... },
      "fraud_detection": { ... },
      "skill_analysis": { ... }
    }
  ]
}
```

### All Candidates Endpoint Response
```json
{
  "total_candidates": 250,
  "showing": 10,
  "skip": 0,
  "limit": 10,
  "global_statistics": {
    "total_applications": 523,
    "total_selected": 145,
    "total_rejected": 298,
    "total_pending": 80
  },
  "candidates": [
    {
      "candidate_profile": { ... },
      "application_summary": { ... },
      "applications": [ ... ]
    },
    {
      "candidate_profile": { ... },
      "application_summary": { ... },
      "applications": [ ... ]
    }
  ]
}
```

## Next Steps

1. Start your backend server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. Test the endpoint with a valid candidate ID

3. Integrate into your frontend application

## Notes

### General
- All datetime fields are returned in ISO 8601 format
- Null values are returned for missing optional fields
- Scores may be null if evaluation hasn't been completed

### Single Candidate Endpoint
- Returns 404 if candidate is not found
- Includes complete resume text in response
- No pagination needed (single candidate)

### All Candidates Endpoint
- Maximum 500 candidates per request (pagination recommended)
- Use skip/limit parameters for efficient pagination
- Global statistics calculated from fetched candidates only
- Empty array returned if no candidates exist
- Ideal for bulk operations and exports
- Can fetch all candidates by incrementing skip parameter

### Performance Tips
- For large datasets, use pagination instead of fetching all at once
- Use the test script's export mode for complete data export
- Limit parameter should be adjusted based on your needs:
  - Small previews: limit=10-20
  - Standard views: limit=50-100
  - Bulk exports: limit=500 (maximum)
