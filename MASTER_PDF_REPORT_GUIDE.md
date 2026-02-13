# Master PDF Report API - Complete Guide

## 📋 Overview

The Master PDF Report API generates a comprehensive, professional-quality PDF report containing complete analytics, rankings, and detailed evaluations for all candidates in your hiring pipeline.

**Endpoint**: `GET /analytics/master-report/pdf`

---

## 🎯 What's Included in the PDF

### 1. **Title Page**
- Report title and generation timestamp
- Metadata table (Total Candidates, Date Generated, Report Type)
- Professional formatting

### 2. **Executive Summary**
- Total candidates processed
- Applications statistics
- Average composite scores
- Selection/Rejection/Pending counts
- **Top 5 Performers Table** with:
  - Candidate name
  - Best application score
  - Number of applications
  - Status (Selected/Rejected/Pending)

### 3. **Individual Candidate Reports**
Each candidate gets a detailed section containing:

#### Candidate Profile
- Personal Information (Name, Email, Mobile)
- Professional Links (LinkedIn, GitHub)
- Years of Experience
- Technical Skills List

#### Application Summary
- Total Applications submitted
- Selected/Rejected/Pending counts
- Average Composite Score
- Best Application highlight

#### Detailed Applications
For EACH application, the report includes:

##### Job Details
- Job Role & Location
- Salary & Employment Type
- Required Experience
- Company Name & Description

##### Comprehensive Scoring
- **Role Fit Score (RFS)**: Skill alignment with job requirements
- **Domain Competency Score (DCS)**: Technical expertise level
- **Experience Level Compatibility (ELC)**: Experience match
- **Composite Score**: Overall weighted score
- **Rank**: Position among all applicants
- **Visual Bar Chart**: Score visualization

##### XAI Explanation
- Why candidate was selected/rejected
- Key strengths identified
- Concerns raised
- Evidence supporting decision
- Recommendation rationale

##### Skill Gap Analysis
- **Matched Skills**: Skills candidate has that job requires
- **Missing Skills**: Required skills candidate lacks
- **Extra Skills**: Bonus skills candidate brings
- Gap percentage and recommendations

##### Fraud Detection
- Fraud flag status
- Similarity index (plagiarism detection)
- Detailed fraud analysis report

##### Skill Evidence Graph
- Skill matching details
- Source document evidence
- Match confidence levels

---

## 🚀 Quick Start

### Using cURL
```bash
# Download PDF for first 20 candidates
curl "http://localhost:8000/analytics/master-report/pdf?limit=20&skip=0" \
  --output candidates_report.pdf

# Production URL
curl "https://agentic-v2-0.onrender.com/analytics/master-report/pdf?limit=10" \
  --output report.pdf
```

### Using Python
```python
import requests

# Generate PDF report
response = requests.get(
    "http://localhost:8000/analytics/master-report/pdf",
    params={"limit": 20, "skip": 0}
)

# Save to file
if response.status_code == 200:
    with open("master_candidate_report.pdf", "wb") as f:
        f.write(response.content)
    print("PDF saved successfully!")
else:
    print(f"Error: {response.status_code}")
```

### Using JavaScript/Fetch
```javascript
// Download PDF in browser
fetch('http://localhost:8000/analytics/master-report/pdf?limit=20')
  .then(response => response.blob())
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'candidates_report.pdf';
    document.body.appendChild(a);
    a.click();
    a.remove();
  });
```

### Using Postman
1. Create new GET request
2. URL: `http://localhost:8000/analytics/master-report/pdf`
3. Add Query Params:
   - `limit`: 20
   - `skip`: 0
4. Click "Send and Download"
5. Save the PDF file

---

## ⚙️ API Parameters

| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `limit` | Integer | 50 | 100 | Maximum number of candidates to include in report |
| `skip` | Integer | 0 | - | Number of candidates to skip (for pagination) |

### Examples:
```bash
# First 10 candidates
GET /analytics/master-report/pdf?limit=10&skip=0

# Next 10 candidates (11-20)
GET /analytics/master-report/pdf?limit=10&skip=10

# Maximum allowed (100 candidates)
GET /analytics/master-report/pdf?limit=100&skip=0

# Candidates 51-100
GET /analytics/master-report/pdf?limit=50&skip=50
```

---

## 📊 Response Details

### Success Response (200 OK)

**Headers:**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename=master_candidate_report_0_20.pdf
Content-Length: [size in bytes]
```

**Body**: Binary PDF file data

### Error Responses

**404 Not Found** - No candidates in database:
```json
{
  "detail": "No candidates found"
}
```

**500 Internal Server Error** - PDF generation failed:
```json
{
  "detail": "Error generating PDF: [error message]"
}
```

---

## 🎨 PDF Features

### Professional Design
- ✅ Clean, modern layout
- ✅ Consistent formatting throughout
- ✅ Proper page breaks between sections
- ✅ Headers and footers
- ✅ Table of contents ready structure

### Visual Elements
- ✅ **Bar Charts**: Score visualization for each application
- ✅ **Tables**: Structured data presentation
- ✅ **Color Coding**: 
  - Scores highlighted with thresholds
  - Status indicators (Selected/Rejected/Pending)
  - Fraud flags in red
- ✅ **Icons & Bullet Points**: Easy scanning

### Data Density
- ✅ Comprehensive but readable
- ✅ Logical information hierarchy
- ✅ Important metrics emphasized
- ✅ Supporting details available

---

## 🔍 Use Cases

### 1. Executive Reports
**Scenario**: CEO wants monthly hiring pipeline overview

```bash
# Generate report for all candidates from last month
curl "https://agentic-v2-0.onrender.com/analytics/master-report/pdf?limit=100" \
  --output monthly_hiring_report.pdf
```

**What they see**:
- Executive summary with top performers
- Key hiring statistics
- Decision quality metrics

### 2. HR Presentation
**Scenario**: HR presenting candidate shortlist to hiring managers

```python
# Generate focused report for top candidates
import requests

response = requests.get(
    "http://localhost:8000/analytics/master-report/pdf",
    params={"limit": 10, "skip": 0}  # Top 10 candidates
)

with open("shortlist_presentation.pdf", "wb") as f:
    f.write(response.content)
```

**What they get**:
- Detailed candidate profiles
- Complete scoring breakdown
- XAI explanations for quick understanding

### 3. Audit & Compliance
**Scenario**: Need documentation for hiring decisions

```bash
# Complete audit trail
curl "http://localhost:8000/analytics/master-report/pdf?limit=100&skip=0" \
  --output hiring_audit_2024.pdf
```

**Compliance covered**:
- All decisions documented
- Fraud detection records
- Unbiased AI scoring evidence

### 4. Candidate Feedback
**Scenario**: Providing detailed feedback to rejected candidates

```python
# Generate individual report (limit=1, skip to specific candidate)
response = requests.get(
    f"http://localhost:8000/analytics/master-report/pdf?limit=1&skip=5"
)
# Send personalized PDF to candidate
```

### 5. Bulk Export
**Scenario**: Quarterly data backup

```bash
# Export all candidates in batches
for i in {0..500..100}; do
  curl "http://localhost:8000/analytics/master-report/pdf?limit=100&skip=$i" \
    --output "candidates_batch_$i.pdf"
done
```

---

## 🛠️ Testing

### Test Script Provided
Run the included test script:

```bash
python test_master_pdf_report.py
```

This will:
- ✅ Test multiple limit values
- ✅ Verify PDF file validity
- ✅ Check file sizes
- ✅ Test edge cases
- ✅ Save sample PDFs

### Manual Testing Checklist

1. **Basic Generation**
   - [ ] PDF downloads successfully
   - [ ] File opens without errors
   - [ ] Title page displays correctly

2. **Content Verification**
   - [ ] Executive summary shows statistics
   - [ ] Top 5 performers table present
   - [ ] All candidates included
   - [ ] Each application has details

3. **Visualizations**
   - [ ] Score bar charts render correctly
   - [ ] Charts match the score values
   - [ ] Images embedded properly

4. **Data Accuracy**
   - [ ] Scores match database values
   - [ ] XAI explanations present
   - [ ] Skill gaps calculated correctly
   - [ ] Fraud flags displayed if present

5. **Edge Cases**
   - [ ] Works with limit=1 (single candidate)
   - [ ] Handles large limits (100+)
   - [ ] Returns 404 with skip > total candidates
   - [ ] Caps limit at 100 maximum

---

## 🚨 Troubleshooting

### PDF won't download
**Problem**: Request times out or fails

**Solutions**:
- Reduce `limit` parameter (try 10-20)
- Check server is running: `GET /health`
- Verify database has candidates
- Check server logs for errors

### PDF is empty or corrupted
**Problem**: File downloads but won't open

**Solutions**:
```python
# Verify PDF header
with open('report.pdf', 'rb') as f:
    header = f.read(4)
    if header == b'%PDF':
        print("Valid PDF")
    else:
        print("Corrupted file")
```

### Missing data in PDF
**Problem**: Some sections are blank

**Solutions**:
- Verify candidates have applications
- Check that applications have been scored
- Ensure XAI explanations were generated
- Run scoring engine: `POST /apply/{job_id}`

### Charts not displaying
**Problem**: Score visualizations missing

**Solutions**:
- Check matplotlib installation: `pip install matplotlib==3.8.2`
- Verify Pillow installed: `pip install Pillow==10.2.0`
- Check server logs for chart generation errors

### Performance issues
**Problem**: PDF takes too long to generate

**Solutions**:
- Reduce limit to 20-30 candidates
- Paginate large exports (multiple requests)
- Consider server resources (CPU/Memory)
- Monitor with: `GET /analytics/company/{id}/dashboard`

---

## 📈 Performance Considerations

### Generation Time
- **1-10 candidates**: ~2-5 seconds
- **10-30 candidates**: ~5-15 seconds
- **30-50 candidates**: ~15-30 seconds
- **50-100 candidates**: ~30-60 seconds

**Factors**:
- Number of applications per candidate
- Chart rendering complexity
- Server CPU/Memory

### File Size
- **Per candidate**: ~50-150 KB
- **10 candidates**: ~500 KB - 1.5 MB
- **50 candidates**: ~2.5 MB - 7.5 MB
- **100 candidates**: ~5 MB - 15 MB

**Optimization**:
- Charts are compressed
- Text efficiently encoded
- Images optimized

### Best Practices
```python
# For large exports, paginate
total_candidates = 250
batch_size = 50

for i in range(0, total_candidates, batch_size):
    response = requests.get(
        "http://localhost:8000/analytics/master-report/pdf",
        params={"limit": batch_size, "skip": i}
    )
    
    filename = f"candidates_{i}_{i+batch_size}.pdf"
    with open(filename, "wb") as f:
        f.write(response.content)
    
    print(f"Saved {filename}")
```

---

## 🔗 Related Endpoints

### Before Generating PDF
1. **Check candidates exist**: `GET /candidate/`
2. **Verify applications scored**: `GET /job/{id}/applications/ranked`
3. **Confirm XAI generated**: `GET /analytics/application/{id}/xai`

### Alternative Data Formats
- **JSON format**: `GET /candidate/master/all` (paginated data)
- **Single candidate**: `GET /candidate/{id}/master`
- **Company dashboard**: `GET /analytics/company/{id}/dashboard`

### After PDF Generation
- **Audit trail**: `GET /candidate/{id}/history`
- **Application details**: `GET /apply/{id}`
- **Rankings**: `GET /analytics/job/{id}/rankings`

---

## 📚 Documentation References

- **Complete API List**: `ALL_APIS_REFERENCE.md`
- **Detailed Endpoints**: `API_ENDPOINTS.md`
- **Master Endpoints**: `MASTER_ENDPOINT_GUIDE.md`
- **Technical Stack**: `TECHNICAL_STACK_AND_ARCHITECTURE.md`
- **Deployment Guide**: `DEPLOYMENT.md`

---

## 💡 Tips & Tricks

### Scheduling Reports
```bash
#!/bin/bash
# Weekly report generation (run with cron)
DATE=$(date +%Y%m%d)
curl "http://localhost:8000/analytics/master-report/pdf?limit=100" \
  --output "reports/weekly_report_$DATE.pdf"
```

### Email Reports
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import requests

# Generate PDF
response = requests.get(
    "http://localhost:8000/analytics/master-report/pdf?limit=20"
)

# Email setup
msg = MIMEMultipart()
msg['Subject'] = 'Weekly Hiring Report'
msg['From'] = 'hr@company.com'
msg['To'] = 'manager@company.com'

# Attach PDF
pdf = MIMEApplication(response.content, _subtype='pdf')
pdf.add_header('Content-Disposition', 'attachment', filename='report.pdf')
msg.attach(pdf)

# Send email
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login('user', 'password')
    server.send_message(msg)
```

### Cloud Storage Upload
```python
import boto3
import requests

# Generate PDF
response = requests.get(
    "http://localhost:8000/analytics/master-report/pdf?limit=50"
)

# Upload to S3
s3 = boto3.client('s3')
s3.put_object(
    Bucket='hiring-reports',
    Key='reports/latest.pdf',
    Body=response.content,
    ContentType='application/pdf'
)
```

---

## 🎓 Advanced Usage

### Custom Filtering
**Coming soon**: Filter by date range, status, score threshold

### Multi-Format Export
```python
# Get both JSON and PDF
json_data = requests.get(
    "http://localhost:8000/candidate/master/all?limit=20"
).json()

pdf_data = requests.get(
    "http://localhost:8000/analytics/master-report/pdf?limit=20"
).content

# Save both
import json
with open('data.json', 'w') as f:
    json.dump(json_data, f)

with open('report.pdf', 'wb') as f:
    f.write(pdf_data)
```

### Streaming Large Reports
```python
import requests

# Stream for memory efficiency
with requests.get(
    "http://localhost:8000/analytics/master-report/pdf?limit=100",
    stream=True
) as response:
    with open('large_report.pdf', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
```

---

## ✅ Summary

The Master PDF Report API provides:
- 📄 **Professional PDF reports** with complete candidate analytics
- 📊 **Visual scoring charts** for easy interpretation
- 🤖 **XAI explanations** for transparent decision-making
- 🔍 **Fraud detection** results for security
- 📈 **Skill gap analysis** for development planning
- 🏆 **Rankings** and top performer identification
- 📋 **Executive summaries** for quick insights
- 💼 **Ready for presentations** to stakeholders

**Perfect for**: HR teams, recruiters, executives, auditors, and anyone needing comprehensive hiring pipeline documentation.

---

**Need help?** Check the interactive docs at `/docs` or contact support.
