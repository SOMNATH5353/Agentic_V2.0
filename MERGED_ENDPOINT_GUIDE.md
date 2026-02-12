# Merged Endpoint: Create Company + Job

## ⭐ New Feature: Single API Call

Instead of making **2 separate API calls**, you can now create both company and job in **1 merged API call**.

---

## 📊 Comparison

### ❌ Old Way (2 API Calls)

#### Step 1: Create Company
```python
import requests

# First API call
response1 = requests.post(
    "https://agentic-v2-0.onrender.com/company/",
    params={
        "name": "TechCorp",
        "description": "Leading technology company"
    }
)
company_id = response1.json()["id"]
```

#### Step 2: Create Job
```python
# Second API call
with open("job_description.pdf", "rb") as f:
    response2 = requests.post(
        "https://agentic-v2-0.onrender.com/job/",
        data={
            "company_id": company_id,  # Need to pass company_id from step 1
            "role": "Python Developer",
            "location": "Remote",
            "salary": "$80k-$120k",
            "employment_type": "Full-time",
            "required_experience": 0
        },
        files={"jd_pdf": f}
    )
```

**Issues**:
- ❌ 2 separate API calls
- ❌ Need to handle company_id manually
- ❌ More error-prone
- ❌ More network overhead

---

### ✅ New Way (1 Merged API Call) - RECOMMENDED

```python
import requests

# Single API call for both!
with open("job_description.pdf", "rb") as f:
    response = requests.post(
        "https://agentic-v2-0.onrender.com/job/create-with-company",
        data={
            # Company details
            "company_name": "TechCorp",
            "company_description": "Leading technology company",
            
            # Job details
            "role": "Python Developer",
            "location": "Remote",
            "salary": "$80k-$120k",
            "employment_type": "Full-time",
            "required_experience": 0
        },
        files={"jd_pdf": f}
    )

result = response.json()
print(f"Company ID: {result['company']['id']}")
print(f"Job ID: {result['job']['id']}")
print(f"Status: {result['company']['status']}")  # "created" or "existing"
```

**Benefits**:
- ✅ Single API call
- ✅ Automatic company creation or reuse
- ✅ Simpler code
- ✅ Atomic operation (both succeed or both fail)
- ✅ Less network overhead

---

## 🔄 Smart Company Handling

The merged endpoint intelligently handles companies:

1. **New Company**: If company name doesn't exist, creates new company
   - Response: `"status": "created"`

2. **Existing Company**: If company name exists, reuses it
   - Response: `"status": "existing"`

This prevents duplicate companies!

---

## 📋 Complete Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| **company_name** | string | ✅ Yes | - | Company name |
| **company_description** | string | ✅ Yes | - | Company description |
| **role** | string | ✅ Yes | - | Job role/title |
| **location** | string | ❌ No | "" | Job location |
| **salary** | string | ❌ No | "" | Salary range |
| **employment_type** | string | ❌ No | "Full-time" | Employment type |
| **required_experience** | integer | ✅ Yes | - | Years of experience |
| **jd_pdf** | file | ✅ Yes | - | Job description PDF |

---

## 📤 Response Structure

```json
{
  "company": {
    "id": 1,
    "name": "TechCorp",
    "description": "Leading technology company",
    "created_at": "2026-02-12T10:00:00",
    "status": "created"  // "created" or "existing"
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
  "skills_extracted": ["python", "flask", "rest api", "docker", "kubernetes"],
  "technical_skills": ["python", "flask", "sql", "git", "docker"],
  "soft_skills": ["communication", "teamwork", "problem solving"]
}
```

---

## 🧪 Testing

Use the provided test script:

```bash
python test_merged_endpoint.py
```

Or test with cURL:

```bash
curl -X POST "https://agentic-v2-0.onrender.com/job/create-with-company" \
  -F "company_name=TechCorp" \
  -F "company_description=Leading AI company" \
  -F "role=Python Developer" \
  -F "location=Remote" \
  -F "salary=$100k-$150k" \
  -F "employment_type=Full-time" \
  -F "required_experience=3" \
  -F "jd_pdf=@job_description.pdf"
```

---

## 🎯 When to Use Which Endpoint?

### Use Merged Endpoint (`/job/create-with-company`) when:
- ✅ Starting fresh with a new company
- ✅ Simplicity is preferred
- ✅ Don't know company ID yet
- ✅ Want automatic duplicate prevention

### Use Separate Endpoints when:
- ✅ Company already exists and you have company_id
- ✅ Creating multiple jobs for same company
- ✅ Need fine-grained control

---

## 📊 Updated API Count

**Total Endpoints: 29** (was 28)

| Category | Old Count | New Count |
|----------|-----------|-----------|
| Job Endpoints | 4 | **5** (+1) |

---

## 🚀 Deployment Status

The merged endpoint is **live and ready to use** at:

```
https://agentic-v2-0.onrender.com/job/create-with-company
```

Interactive Documentation:
- Swagger UI: https://agentic-v2-0.onrender.com/docs
- ReDoc: https://agentic-v2-0.onrender.com/redoc

---

## ✨ Summary

The new merged endpoint provides:
1. **Simpler workflow**: 1 API call instead of 2
2. **Smart handling**: Automatic company creation or reuse
3. **Better UX**: Less complexity for frontend developers
4. **Atomic operations**: Both operations succeed or fail together
5. **Backward compatible**: Old endpoints still work

**Recommendation**: Use the merged endpoint for new integrations! ⭐
