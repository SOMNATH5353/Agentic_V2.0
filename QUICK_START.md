# 🚀 Quick Start Guide - Agentic AI Hiring Platform

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
# Required:
# - DATABASE_URL (PostgreSQL connection string)
# - HF_API_KEY (HuggingFace API key)
```

### Step 3: Start the Server
```bash
uvicorn app.main:app --reload
```

Server will start at: **http://127.0.0.1:8000**

### Step 4: Access API Documentation
Open in browser: **http://127.0.0.1:8000/docs**

---

## 📝 Basic Usage Flow

### 1. Create a Company
```http
POST /company/
Content-Type: application/json

{
  "name": "Tech Corp",
  "description": "Leading technology company"
}
```

### 2. Create a Job Posting
```http
POST /job/
Content-Type: multipart/form-data

company_id: 1
role: Senior Python Developer
salary: $120k-$150k
required_experience: 5
jd_pdf: [Upload PDF file]
```

### 3. Submit an Application
```http
POST /apply/1
Content-Type: multipart/form-data

name: John Doe
email: john@example.com
linkedin: linkedin.com/in/johndoe
github: github.com/johndoe
experience: 6
resume_pdf: [Upload PDF file]
```

### 4. View Results
```http
GET /apply/1

Response:
{
  "decision": "Fast-Track Selected",
  "composite_score": 0.87,
  "explanation": { ... },
  "skill_match": { ... }
}
```

---

## 🔑 Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info |
| `/docs` | GET | Swagger UI |
| `/company/` | POST | Create company |
| `/job/` | POST | Create job (upload PDF) |
| `/job/{id}/applications` | GET | View job applications |
| `/apply/{job_id}` | POST | Submit application (upload PDF) |
| `/apply/{id}` | GET | Get application details |
| `/candidate/{id}` | GET | Get candidate profile |

---

## 📊 Decision Categories

| Decision | Score Range | Meaning |
|----------|-------------|---------|
| **Fast-Track Selected** | ≥ 0.85 | Excellent match - interview immediately |
| **Selected** | 0.75 - 0.84 | Strong candidate - schedule interview |
| **Hire-Pooled** | 0.60 - 0.74 | Moderate fit - talent pool |
| **Rejected** | < 0.60 | Insufficient match |
| **Review Required** | Any | Fraud detected or edge case |

---

## 🎯 Understanding Scores

### Composite Score = (RFS × 0.4) + (DCS × 0.4) + (ELC × 0.2)

- **RFS**: Role Fit Score (semantic similarity)
- **DCS**: Domain Competency Score (skill matching)
- **ELC**: Experience Level Compatibility

---

## 🔍 Example Response

```json
{
  "application_id": 1,
  "decision": "Selected",
  "composite_score": 0.78,
  "scores": {
    "rfs": 0.82,
    "dcs": 0.75,
    "elc": 1.0
  },
  "skill_match": {
    "match_percentage": 75.0,
    "matched_skills": ["python", "fastapi", "postgresql"],
    "missing_skills": ["kubernetes", "docker"],
    "matched_count": 15,
    "total_required": 20
  },
  "explanation": {
    "summary": "Strong candidate with composite score of 0.78...",
    "strengths": [
      "Good role alignment",
      "Meets experience requirements"
    ],
    "weaknesses": [
      "Missing skills: kubernetes, docker"
    ],
    "recommendation": "✅ Schedule interview"
  },
  "fraud_detection": {
    "fraud_flag": false,
    "risk_level": "none"
  }
}
```

---

## 🛠️ Testing the Platform

### Using the Swagger UI (`/docs`):

1. Click on an endpoint
2. Click "Try it out"
3. Fill in parameters
4. For file uploads: Click "Choose File" and select PDF
5. Click "Execute"
6. View response below

### Using cURL:

```bash
# Create job
curl -X POST "http://127.0.0.1:8000/job/" \
  -F "company_id=1" \
  -F "role=Python Developer" \
  -F "salary=$100k" \
  -F "required_experience=3" \
  -F "jd_pdf=@job_description.pdf"

# Submit application
curl -X POST "http://127.0.0.1:8000/apply/1" \
  -F "name=John Doe" \
  -F "email=john@example.com" \
  -F "experience=5" \
  -F "resume_pdf=@resume.pdf"
```

---

## ⚡ Quick Tips

1. **PDF Files**: Must be actual PDF format, not scanned images
2. **Email Uniqueness**: Each candidate email can only apply once per job
3. **Skills**: System recognizes 200+ technical skills automatically
4. **Fraud Detection**: Resumes with >90% similarity are flagged
5. **Explanations**: Every decision includes detailed reasoning

---

## 🐛 Common Issues

### Server won't start
- Check `.env` file exists and DATABASE_URL is correct
- Ensure PostgreSQL is running and accessible

### PDF parsing fails
- Ensure PDF is text-based, not scanned image
- Check file size (recommend < 10MB)

### Low skill match despite good resume
- Add domain-specific skills to `inference_engine.py`
- Check JD has clear skill requirements

---

## 📈 Monitoring

### Check system health
```bash
curl http://127.0.0.1:8000/health
```

### View application statistics
```bash
curl http://127.0.0.1:8000/job/1/applications
```

### Check fraud flags
```bash
curl "http://127.0.0.1:8000/apply/?fraud_flag=true"
```

---

## 🎓 Learning Resources

- **Full Documentation**: `backend/README.md`
- **API Reference**: `http://127.0.0.1:8000/docs`
- **Improvements Summary**: `IMPROVEMENTS_SUMMARY.md`
- **Code Examples**: Available in `/docs` endpoint

---

## 📞 Need Help?

1. Check the Swagger UI documentation at `/docs`
2. Review audit logs for debugging: `GET /apply/{id}/history`
3. Check application explanations: `GET /apply/{id}`
4. Review `backend/README.md` for detailed information

---

## ✅ Success Checklist

- [ ] Server starts without errors
- [ ] Can access `/docs` endpoint
- [ ] Created at least one company
- [ ] Created at least one job with PDF
- [ ] Submitted at least one application with PDF
- [ ] Received evaluation results
- [ ] Reviewed explanation details

---

**🎉 You're ready to use the Agentic AI Hiring Platform!**

For advanced features and production deployment, see `backend/README.md`
