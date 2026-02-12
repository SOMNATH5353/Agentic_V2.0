# Quick Deployment Guide - Render

## 🚀 Deploy in 5 Minutes

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Deploy to Render"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Deploy on Render

#### Option A: One-Click Blueprint (Easiest)
1. Log in to [render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repo
4. Render detects `render.yaml` automatically
5. Add `HF_API_KEY` when prompted
6. Click **"Apply"**
7. ✅ Done! Wait 3-5 minutes for deployment

#### Option B: Manual Setup
1. **Create Database**:
   - New + → PostgreSQL
   - Name: `agentic-hiring-db`
   - Free plan → Create

2. **Create Web Service**:
   - New + → Web Service
   - Connect GitHub repo
   - Root directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   
3. **Add Environment Variables**:
   ```
   DATABASE_URL=[from database dashboard]
   HF_API_KEY=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
   SIMILARITY_THRESHOLD=0.90
   ```

4. ✅ Deploy!

### 3. Test Your Deployment

```bash
# Replace with your actual URL
export API_URL=https://your-app.onrender.com

# Test health check
curl $API_URL/health

# Open docs
open $API_URL/docs
```

---

## 📝 Environment Variables Needed

| Variable | Value | Where to Get |
|----------|-------|--------------|
| `DATABASE_URL` | Auto-set by Render | Created automatically |
| `HF_API_KEY` | Your HuggingFace token | [Get here](https://huggingface.co/settings/tokens) |
| `SIMILARITY_THRESHOLD` | `0.90` | Default value |

---

## 🔗 Your App URLs

After deployment:
- **API**: `https://your-service.onrender.com`
- **Docs**: `https://your-service.onrender.com/docs`
- **Health**: `https://your-service.onrender.com/health`

---

## 💰 Cost

- **Free Tier**: $0/month (sleeps after 15 min inactivity)
- **Starter**: $14/month (always on, recommended)

---

## 🐛 Troubleshooting

**Service won't start?**
- Check logs in Render dashboard
- Verify `HF_API_KEY` is set
- Ensure `requirements.txt` is in `backend/` folder

**Database connection failed?**
- Verify `DATABASE_URL` is set
- Check database is running

**Cold starts taking long?**
- Free tier sleeps after 15 min
- Upgrade to Starter plan ($7/month) for always-on

---

## 📚 Full Documentation

- [Complete Deployment Guide](./DEPLOYMENT.md)
- [API Endpoints Documentation](./backend/API_ENDPOINTS.md)
- [Deployment Checklist](./DEPLOYMENT_CHECKLIST.md)

---

**Need Help?**
- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
