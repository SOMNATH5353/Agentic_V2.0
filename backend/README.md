# 🤖 Agentic AI Hiring & Talent Evaluation Platform V2.0

## 📋 Overview

An intelligent, end-to-end AI-powered hiring platform that evaluates candidates based on comprehensive skill matching, experience compatibility, and fraud detection. The system provides explainable, auditable hiring decisions using advanced NLP and machine learning techniques.

### 🎯 Key Features

- ✅ **PDF Resume & JD Processing** - Upload and parse PDF documents
- 🧠 **AI-Powered Skill Extraction** - Automatically extract 200+ technical & soft skills
- 📊 **Multi-Factor Scoring System** - RFS, DCS, ELC, and Composite scores
- 🔍 **Advanced Fraud Detection** - Multi-level resume duplication detection
- 💡 **Explainable AI Decisions** - Detailed reasoning for every hiring decision
- 📝 **Complete Audit Trail** - Track all evaluations and decisions
- 🏢 **Multi-Company Support** - Manage multiple companies and job postings
- 🔄 **Scalable Architecture** - Production-ready with PostgreSQL + SQLAlchemy

---

## 🏗️ Architecture

### Tech Stack

- **Backend**: Python 3.13, FastAPI
- **Database**: PostgreSQL (Neon Cloud)
- **ORM**: SQLAlchemy
- **AI/ML**: HuggingFace Inference API
- **NLP**: Custom skill extraction, cosine similarity
- **PDF Processing**: PyPDF2

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Backend                       │
├─────────────────────────────────────────────────────────┤
│  Routes          │  Core Pipeline  │  Services          │
│  - Company       │  - Evaluation   │  - Scoring Engine  │
│  - Job           │  - Processing   │  - Fraud Detection │
│  - Application   │  - Audit        │  - Explanation AI  │
│  - Candidate     │                 │  - Inference Engine│
├─────────────────────────────────────────────────────────┤
│              SQLAlchemy ORM + PostgreSQL                 │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Database Schema

### Tables

1. **Companies** - Organization details
2. **Jobs** - Job postings with JD embeddings
3. **Candidates** - Applicant profiles with resume embeddings
4. **Applications** - Evaluation results and decisions
5. **Audit Logs** - Complete activity tracking

### Relationships

```
Company (1) ──→ (N) Jobs
Jobs (1) ──→ (N) Applications
Candidates (1) ──→ (N) Applications
Applications (N) ──→ (N) Audit Logs
```

---

## 🧠 AI Evaluation Logic

### 1. Role Fit Score (RFS) - 40% Weight

**Semantic similarity between JD and Resume**
- Uses HuggingFace sentence-transformers/all-MiniLM-L6-v2
- Cosine similarity of embeddings
- Range: 0.0 to 1.0

### 2. Domain Competency Score (DCS) - 40% Weight

**Actual skill matching**
- Extracts 200+ technical skills (Python, AWS, React, etc.)
- Identifies soft skills (leadership, communication, etc.)
- Computes match percentage
- Formula: `matched_skills / (required_skills + 0.5 * missing_skills)`

### 3. Experience Level Compatibility (ELC) - 20% Weight

**Experience requirement matching**
- Perfect match: candidate_exp >= required_exp → 1.0
- Close match: candidate_exp >= 75% of required → 0.8
- Moderate: candidate_exp >= 50% of required → 0.5
- Below threshold → 0.0
- Overqualification penalty: >2.5x experience → 0.9x

### 4. Composite Score

```python
composite = 0.40 * RFS + 0.40 * DCS + 0.20 * ELC
```

---

## 🚨 Fraud Detection System

### Multi-Level Checks

1. **Embedding Similarity** - Detects semantic duplication
   - Threshold: 90% (configurable)
   - Compares against all existing resumes

2. **Text Duplication** - Character-level n-gram analysis
   - Jaccard similarity index
   - Detects copy-paste attempts

3. **Email Duplication** - Prevents resubmissions

4. **Template Detection** - Identifies placeholder text
   - Checks for generic phrases
   - Flags incomplete resumes

### Risk Levels

- **Critical**: Similarity > 95% or multiple red flags
- **High**: Similarity > 92% or 2+ risk factors
- **Medium**: Similarity > 85% or 1 risk factor
- **Low**: Minor indicators
- **None**: Clean

---

## 📈 Decision Logic

### Automatic Classifications

| Composite Score | Experience | Fraud | Decision |
|----------------|-----------|-------|----------|
| >= 0.85 | ✓ | ✗ | **Fast-Track Selected** |
| >= 0.75 | ✓ | ✗ | **Selected** |
| >= 0.60 | ✓ | Minor | **Hire-Pooled** |
| < 0.60 | ✗ | Any | **Rejected** |
| Any | Any | High | **Review Required** |

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.13+
- PostgreSQL database (or Neon Cloud account)
- HuggingFace API key

### Step 1: Clone & Navigate

```bash
cd backend
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment

Create `.env` file in `backend/` directory:

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
HF_API_KEY=your_huggingface_api_key
SIMILARITY_THRESHOLD=0.90
```

### Step 4: Run Server

```bash
cd backend
uvicorn app.main:app --reload
```

Server starts at: `http://127.0.0.1:8000`

### Step 5: Access API Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 📡 API Endpoints

### Company Management

- `POST /company/` - Create company
- `GET /company/{id}` - Get company details

### Job Management

- `POST /job/` - Create job (upload JD PDF)
- `GET /job/{id}` - Get job details
- `GET /job/{id}/applications` - Get all applications for job
- `GET /job/` - List all jobs (with filters)

### Application Submission

- `POST /apply/{job_id}` - Submit application (upload resume PDF)
- `GET /apply/{id}` - Get application details with explanation
- `GET /apply/{id}/history` - Get audit history
- `GET /apply/` - List applications (with filters)

### Candidate Management

- `GET /candidate/{id}` - Get candidate profile
- `GET /candidate/{id}/applications` - Get all applications
- `GET /candidate/{id}/history` - Get complete history
- `GET /candidate/search/by-email?email=` - Search by email

---

## 💻 Usage Examples

### 1. Create a Job Posting

```bash
curl -X POST "http://127.0.0.1:8000/job/" \
  -H "Content-Type: multipart/form-data" \
  -F "company_id=1" \
  -F "role=Senior Python Developer" \
  -F "salary=$120k-$150k" \
  -F "required_experience=5" \
  -F "jd_pdf=@job_description.pdf"
```

### 2. Submit Application

```bash
curl -X POST "http://127.0.0.1:8000/apply/1" \
  -H "Content-Type: multipart/form-data" \
  -F "name=John Doe" \
  -F "email=john@example.com" \
  -F "linkedin=linkedin.com/in/johndoe" \
  -F "github=github.com/johndoe" \
  -F "experience=6" \
  -F "resume_pdf=@resume.pdf"
```

### 3. Get Application Details

```bash
curl "http://127.0.0.1:8000/apply/1"
```

---

## 📤 Example Output

```json
{
  "application_id": 1,
  "candidate_id": 42,
  "job_id": 1,
  "decision": "Fast-Track Selected",
  "composite_score": 0.87,
  "scores": {
    "rfs": 0.89,
    "dcs": 0.85,
    "elc": 1.0
  },
  "skill_match": {
    "match_percentage": 85.0,
    "matched_skills": ["python", "fastapi", "postgresql", "docker", "aws"],
    "missing_skills": ["kubernetes"],
    "matched_count": 17,
    "total_required": 20
  },
  "explanation": {
    "summary": "Exceptional candidate with composite score of 0.87. Immediate interview recommended.",
    "strengths": [
      "Excellent role fit with 89% semantic alignment",
      "Strong skill match: 17 required skills present",
      "Meets experience requirements (6 years)"
    ],
    "weaknesses": [
      "Missing key skills: kubernetes"
    ],
    "recommendation": "✅ Immediately schedule interview. Excellent candidate match.",
    "confidence_level": {
      "level": "high",
      "score": 0.9
    }
  },
  "fraud_detection": {
    "fraud_flag": false,
    "risk_level": "none",
    "similarity_index": 0.12
  }
}
```

---

## 🔧 Advanced Configuration

### Custom Scoring Weights

In `scoring_engine.py`:

```python
weights = {
    "rfs": 0.40,  # Role fit
    "dcs": 0.40,  # Skill match
    "elc": 0.20   # Experience
}
```

### Fraud Detection Thresholds

In `.env`:

```env
SIMILARITY_THRESHOLD=0.90
```

In `fraud_detection.py`:

```python
self.high_risk_threshold = 0.92
self.medium_risk_threshold = 0.85
```

---

## 📊 Monitoring & Analytics

### Audit Trail Queries

```python
# Get evaluation history
from app.services.audit_service import AuditService

# Application history
history = AuditService.get_application_history(db, application_id)

# Fraud flags
frauds = AuditService.get_fraud_flags(db, limit=50)

# Time-based report
report = AuditService.generate_audit_report(db, start_date, end_date)
```

---

## 🎯 Production Deployment Checklist

- [ ] Set strong `DATABASE_URL` with SSL
- [ ] Rotate `HF_API_KEY` regularly
- [ ] Enable CORS with specific origins
- [ ] Add rate limiting (e.g., slowapi)
- [ ] Set up database backups
- [ ] Configure logging (e.g., loguru)
- [ ] Add authentication & authorization
- [ ] Use environment-specific configs
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Add caching layer (Redis)
- [ ] Implement async processing for large PDFs
- [ ] Add file size limits
- [ ] Set up CI/CD pipeline

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** - Use `.env.example` template
2. **Validate all file uploads** - Check file types and sizes
3. **Sanitize PDF inputs** - Prevent malicious content
4. **Use parameterized queries** - SQLAlchemy handles this
5. **Implement rate limiting** - Prevent abuse
6. **Add authentication** - JWT tokens or OAuth2
7. **Enable HTTPS** - Use reverse proxy (nginx)

---

## 🐛 Troubleshooting

### Issue: Database Connection Error

```
sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URL
```

**Solution**: Check `.env` file - ensure `DATABASE_URL` has correct format:
```
DATABASE_URL=postgresql://user:pass@host:5432/db
```

### Issue: PDF Parsing Fails

**Solution**: Ensure PyPDF2 is installed and PDF is not encrypted/password-protected.

### Issue: Low Skill Match

**Solution**: Check `inference_engine.py` - add domain-specific skills to `TECHNICAL_SKILLS` set.

---

## 📈 Future Enhancements

### Phase 3 Roadmap

- [ ] **pgvector Integration** - Faster similarity search
- [ ] **Background Processing** - Celery task queue
- [ ] **Advanced NLP** - Named Entity Recognition
- [ ] **Multi-Language Support** - Translate JDs/resumes
- [ ] **Video Interview Analysis** - CV-based evaluation
- [ ] **Bias Detection** - Fair hiring metrics
- [ ] **Custom Workflows** - Configurable pipelines
- [ ] **Integration APIs** - ATS system connectors
- [ ] **Real-time Notifications** - WebSocket updates
- [ ] **Analytics Dashboard** - Hiring insights

---

## 📚 API Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 404 | Not Found (resource doesn't exist) |
| 500 | Internal Server Error |

---

## 🤝 Contributing

This is a production-ready platform. For enhancements:

1. Review the architecture
2. Check existing services
3. Add comprehensive tests
4. Update documentation
5. Follow existing patterns

---

## 📄 License

Proprietary - All Rights Reserved

---

## 📞 Support

For issues or questions:
- Check `/docs` endpoint for API reference
- Review audit logs for debugging
- Check application explanations for decision reasoning

---

## 🎓 System Insights

### Why This Architecture?

1. **Modular Services** - Easy to test, maintain, and extend
2. **Explainable AI** - Every decision is transparent
3. **Audit Trail** - Complete compliance and debugging
4. **Scalable** - Handles 1000s of applications
5. **Production-Ready** - Error handling, validation, logging

### Performance Optimization

- **Embedding caching** - Store embeddings in DB
- **Batch processing** - Evaluate multiple candidates together
- **Async operations** - Non-blocking PDF processing
- **Database indexing** - Fast queries on common fields
- **Connection pooling** - Efficient DB connections

---

## 🌟 Success Metrics

Track these KPIs:

- **Evaluation Time** - < 5 seconds per application
- **Fraud Detection Rate** - % of duplicates caught
- **False Positives** - Legitimate candidates flagged
- **Decision Confidence** - Average confidence scores
- **Skill Match Accuracy** - Recruiter agreement rate

---

**Built with ❤️ using FastAPI, SQLAlchemy, and AI**
