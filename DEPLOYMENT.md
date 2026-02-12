# Deployment Guide - Render.com

This guide will help you deploy the Agentic AI Hiring Platform V2.0 to Render.com.

---

## Prerequisites

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com) (free tier available)
3. **HuggingFace API Key** - Get from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

---

## Method 1: Deploy Using Render Blueprint (Recommended)

### Step 1: Push Code to GitHub

```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit - Agentic AI Hiring Platform"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy from Render Dashboard

1. **Log in to Render**: Go to [dashboard.render.com](https://dashboard.render.com)

2. **Create New Blueprint**:
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub account if not already connected
   - Select your repository
   - Render will automatically detect `render.yaml`

3. **Configure Environment Variables**:
   - Render will create both the web service and PostgreSQL database
   - You'll be prompted to add `HF_API_KEY`
   - Add your HuggingFace API key: `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`

4. **Deploy**:
   - Click **"Apply"**
   - Render will:
     - Create PostgreSQL database
     - Create web service
     - Install dependencies
     - Start your application

5. **Wait for Deployment** (3-5 minutes):
   - Monitor logs in Render dashboard
   - Once complete, you'll get a URL like: `https://agentic-hiring-backend.onrender.com`

---

## Method 2: Manual Deployment

### Step 1: Create PostgreSQL Database

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `agentic-hiring-db`
   - **Database**: `agentic_hiring`
   - **Region**: Singapore (or closest to you)
   - **Plan**: Free (or Starter for production)
3. Click **"Create Database"**
4. **Copy the Internal Database URL** (starts with `postgresql://`)

### Step 2: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `agentic-hiring-backend`
   - **Region**: Singapore (same as database)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4`

4. **Add Environment Variables**:
   ```
   DATABASE_URL=<paste Internal Database URL from Step 1>
   HF_API_KEY=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
   SIMILARITY_THRESHOLD=0.90
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   PYTHON_VERSION=3.11.0
   ```

5. **Select Plan**: Free (or Starter for production)

6. Click **"Create Web Service"**

---

## Step 3: Verify Deployment

Once deployment completes:

1. **Open Application URL**: `https://your-service-name.onrender.com`

2. **Test Health Endpoint**:
   ```bash
   curl https://your-service-name.onrender.com/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "service": "Agentic AI Hiring Platform",
     "version": "2.0.0"
   }
   ```

3. **Access API Documentation**:
   - Swagger UI: `https://your-service-name.onrender.com/docs`
   - ReDoc: `https://your-service-name.onrender.com/redoc`

---

## Step 4: Initialize Database

The database tables will be created automatically on first startup (via SQLAlchemy).

If you need to run migrations manually:

1. **Access Shell** in Render dashboard
2. Run:
   ```bash
   python migrate_db.py
   ```

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | ✅ Yes | - | PostgreSQL connection string (auto-set by Render) |
| `HF_API_KEY` | ✅ Yes | - | HuggingFace API key for embeddings |
| `SIMILARITY_THRESHOLD` | ❌ No | 0.90 | Fraud detection similarity threshold |
| `ENVIRONMENT` | ❌ No | development | Environment (development/production) |
| `LOG_LEVEL` | ❌ No | INFO | Logging level |
| `PYTHON_VERSION` | ❌ No | 3.11.0 | Python version |

### Update Environment Variables

1. Go to your web service in Render dashboard
2. Click **"Environment"** tab
3. Add/edit variables
4. Service will automatically redeploy

---

## Monitoring & Logs

### View Logs

1. Go to your web service in Render dashboard
2. Click **"Logs"** tab
3. Monitor real-time application logs

### View Metrics

1. Click **"Metrics"** tab
2. Monitor:
   - CPU usage
   - Memory usage
   - Response times
   - Request rates

### Health Checks

Render automatically monitors `/health` endpoint:
- If endpoint fails, service will be restarted
- Configure in **"Settings"** → **"Health Check Path"**

---

## Scaling

### Free Tier Limitations

- **Spins down after 15 minutes of inactivity**
- First request after sleep: 30-60 seconds cold start
- 750 hours/month free

### Upgrade for Production

1. **Starter Plan** ($7/month):
   - No sleep / always active
   - Faster CPU
   - More memory

2. **Database Upgrade** ($7/month):
   - More storage
   - Higher connection limits
   - Automated backups

### Horizontal Scaling

Modify `--workers` in start command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 8
```

---

## Automatic Deployments

### Enable Auto-Deploy

1. In Render dashboard, go to service settings
2. Enable **"Auto-Deploy"**
3. Every push to `main` branch will trigger deployment

### Manual Deploy

1. Go to service in Render dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## Custom Domain (Optional)

1. Go to service **"Settings"**
2. Scroll to **"Custom Domains"**
3. Click **"Add Custom Domain"**
4. Follow instructions to configure DNS

Example: `api.yourdomain.com`

---

## Database Backups

### Free Tier
- Manual backups only
- Download from dashboard

### Paid Plans
- Automatic daily backups
- Point-in-time recovery
- Backup retention: 7-30 days

### Manual Backup

```bash
# From your local machine
pg_dump $DATABASE_URL > backup.sql
```

---

## Troubleshooting

### Service Won't Start

**Check logs for errors**:
1. Go to **"Logs"** tab in dashboard
2. Look for error messages

**Common issues**:
- Missing environment variables
- Database connection failed
- Port already in use (should use `$PORT` variable)

### Database Connection Issues

1. Verify `DATABASE_URL` is set correctly
2. Check database is in same region as web service
3. Verify PostgreSQL service is running in dashboard

### Slow Performance

1. **Cold starts** (free tier): Wait 30-60 seconds on first request
2. Upgrade to Starter plan for always-on service
3. Increase workers: `--workers 4` or higher

### Out of Memory

1. Check logs for memory errors
2. Upgrade to higher memory plan
3. Optimize code to use less memory

---

## API Testing After Deployment

### Using cURL

```bash
# Health check
curl https://your-service.onrender.com/health

# Create company
curl -X POST "https://your-service.onrender.com/company/" \
  -d "name=TechCorp" \
  -d "description=Leading tech company"

# Upload job description
curl -X POST "https://your-service.onrender.com/job/" \
  -F "company_id=1" \
  -F "role=Python Developer" \
  -F "location=Remote" \
  -F "required_experience=0" \
  -F "jd_pdf=@job_description.pdf"

# Submit application
curl -X POST "https://your-service.onrender.com/apply/1" \
  -F "name=John Doe" \
  -F "email=john@example.com" \
  -F "mobile=1234567890" \
  -F "experience=2" \
  -F "resume_pdf=@resume.pdf"
```

### Using Python

```python
import requests

BASE_URL = "https://your-service.onrender.com"

# Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Create company
response = requests.post(
    f"{BASE_URL}/company/",
    params={"name": "TechCorp", "description": "Tech company"}
)
print(response.json())
```

---

## Cost Estimation

### Free Tier (Hobby)
- Web Service: **$0/month** (with sleep)
- PostgreSQL: **$0/month** (limited storage)
- **Total**: $0/month

### Production Setup (Starter)
- Web Service: **$7/month** (always on)
- PostgreSQL: **$7/month** (automated backups)
- **Total**: $14/month

### Scaling (Standard)
- Web Service: **$25/month** (2 CPU cores, 2GB RAM)
- PostgreSQL: **$20/month** (more storage, connections)
- **Total**: $45/month

---

## Security Best Practices

1. **Environment Variables**: Never commit `.env` to git
2. **HTTPS**: Render provides free SSL certificates
3. **Database**: Use internal connection string for best security
4. **API Keys**: Rotate HuggingFace API key periodically
5. **CORS**: Update `main.py` to restrict origins in production:
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

---

## Support & Resources

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Render Status**: [status.render.com](https://status.render.com)
- **Community**: [community.render.com](https://community.render.com)
- **Support**: Email support@render.com

---

## Next Steps After Deployment

1. ✅ Test all API endpoints
2. ✅ Set up monitoring/alerts
3. ✅ Configure custom domain (optional)
4. ✅ Set up CI/CD pipeline
5. ✅ Implement rate limiting
6. ✅ Add authentication (JWT)
7. ✅ Set up error tracking (Sentry)
8. ✅ Create frontend application
9. ✅ Load test the application
10. ✅ Set up automated backups

---

## Rollback

If deployment fails:

1. Go to **"Events"** tab in Render dashboard
2. Find previous successful deployment
3. Click **"Rollback"**
4. Service will revert to previous version

---

## Questions?

- Check [API_ENDPOINTS.md](./backend/API_ENDPOINTS.md) for API documentation
- Review logs in Render dashboard
- Contact Render support for platform issues

**Your app is now live! 🚀**

Access at: `https://your-service-name.onrender.com`
