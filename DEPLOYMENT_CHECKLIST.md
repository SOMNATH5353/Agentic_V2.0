# Render Deployment Checklist

## Pre-Deployment

- [ ] Code is in a GitHub repository
- [ ] All environment variables documented in `.env.example`
- [ ] `requirements.txt` is up to date
- [ ] Database migrations are ready (if using Alembic)
- [ ] Health check endpoint (`/health`) is working
- [ ] API documentation is accessible at `/docs`

## Deployment Setup

- [ ] Render account created at [render.com](https://render.com)
- [ ] HuggingFace API key obtained from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- [ ] GitHub repository connected to Render

## Render Configuration

### Blueprint Method (Recommended)
- [ ] `render.yaml` exists in project root
- [ ] Pushed code to GitHub
- [ ] Created new Blueprint in Render
- [ ] Added `HF_API_KEY` environment variable
- [ ] Clicked "Apply" to deploy

### Manual Method
- [ ] Created PostgreSQL database in Render
- [ ] Copied internal database URL
- [ ] Created web service in Render
- [ ] Configured build command: `pip install -r requirements.txt`
- [ ] Configured start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4`
- [ ] Added all environment variables:
  - [ ] `DATABASE_URL`
  - [ ] `HF_API_KEY`
  - [ ] `SIMILARITY_THRESHOLD`
  - [ ] `ENVIRONMENT=production`
  - [ ] `LOG_LEVEL=INFO`

## Post-Deployment

### Testing
- [ ] Health check works: `https://your-service.onrender.com/health`
- [ ] API docs accessible: `https://your-service.onrender.com/docs`
- [ ] Create company endpoint works
- [ ] Create job endpoint works
- [ ] Submit application endpoint works
- [ ] Analytics endpoints working

### Monitoring
- [ ] Service logs are visible in dashboard
- [ ] Health check monitoring is active
- [ ] Metrics are being collected

### Optional Enhancements
- [ ] Custom domain configured
- [ ] Auto-deploy enabled for main branch
- [ ] Database backups configured
- [ ] Error tracking (Sentry) set up
- [ ] Rate limiting implemented
- [ ] Authentication (JWT) added
- [ ] CORS configured for production domain

## Production Ready

- [ ] All API endpoints tested in production
- [ ] Performance tested with realistic load
- [ ] Security best practices followed
- [ ] Monitoring and alerts configured
- [ ] Backup strategy in place
- [ ] Documentation updated with production URL

## Your Service URLs

After deployment, fill in:

- **API Base URL**: `https://_____.onrender.com`
- **API Documentation**: `https://_____.onrender.com/docs`
- **Health Check**: `https://_____.onrender.com/health`
- **Database**: Internal URL in Render dashboard

## Troubleshooting

If deployment fails, check:

1. **Logs** in Render dashboard for error messages
2. **Environment variables** are all set correctly
3. **Database connection** is working
4. **Python version** matches requirements (3.11+)
5. **Dependencies** install successfully

## Support

- Render Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com
- Full deployment guide: See [DEPLOYMENT.md](./DEPLOYMENT.md)

---

**Last Updated**: February 12, 2026
**Version**: 2.0.0
