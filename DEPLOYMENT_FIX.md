# Render Deployment - Quick Fix Guide

## ✅ Issue Fixed

The deployment was failing because Render was looking for a Dockerfile. I've now created:
1. **Dockerfile** - Docker container configuration
2. **.dockerignore** - Files to exclude from Docker build
3. **Updated render.yaml** - Now uses Docker runtime

---

## 🚀 Deploy Again (Updated Steps)

### Step 1: Ensure Branch is Correct

Your repo uses **main** branch, but you might be on **master**. Let's sync:

```bash
# Check current branch
git branch

# If on master, switch to main and merge
git checkout main
git merge master
git push origin main

# Or if you want to use master as main:
git branch -M main
git push -f origin main
```

### Step 2: Push New Files

```bash
# Add new Docker files
git add Dockerfile .dockerignore render.yaml
git commit -m "Add Docker support for Render deployment"
git push origin main
```

### Step 3: Deploy on Render

#### Option A: Blueprint (Recommended)
1. Go to [dashboard.render.com](https://dashboard.render.com)
2. **Delete the failed service** if it exists
3. Click **"New +"** → **"Blueprint"**
4. Select your repository: `SOMNATH5353/Agentic_V2.0`
5. Render will detect `render.yaml` automatically
6. Add environment variable:
   - **Key**: `HF_API_KEY`
   - **Value**: `hf_YOUR_TOKEN_HERE` (use your actual token)
7. Click **"Apply"**

#### Option B: Manual Docker Deploy
If Blueprint doesn't work, try manual setup:

1. **Create Database First**:
   - New + → PostgreSQL
   - Name: `agentic-hiring-db`
   - Database: `agentic_hiring`
   - Region: Singapore
   - Plan: Free
   - Create

2. **Create Web Service**:
   - New + → Web Service
   - Connect to your GitHub repository
   - **Build Source**: Use Dockerfile
   - **Dockerfile Path**: `./Dockerfile`
   - Region: Singapore
   - Branch: `main`
   
3. **Environment Variables**:
   ```
   DATABASE_URL=[copy from database internal connection string]
   HF_API_KEY=hf_YOUR_TOKEN_HERE
   SIMILARITY_THRESHOLD=0.90
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   ```

4. **Deploy**

---

## 🔍 What Changed

### Before (Failed)
```yaml
runtime: python
buildCommand: pip install -r requirements.txt
startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### After (Fixed)
```yaml
runtime: docker
dockerfilePath: ./Dockerfile
# Docker handles build and start automatically
```

---

## 📦 Dockerfile Details

The Dockerfile:
- ✅ Uses Python 3.11 slim image
- ✅ Installs dependencies
- ✅ Copies only backend code
- ✅ Runs with 4 workers
- ✅ Sets up health checks
- ✅ Uses non-root user for security

---

## 🐛 If Still Failing

### Check These:

1. **Branch Name**:
   ```bash
   git branch --show-current
   # Should show: main
   ```

2. **Files Pushed**:
   ```bash
   git ls-files | grep -E "(Dockerfile|render.yaml)"
   # Should show both files
   ```

3. **Render Logs**:
   - Go to your service in Render
   - Check "Logs" tab
   - Look for specific error messages

### Common Errors:

**"Failed to read dockerfile"**
- Solution: Make sure Dockerfile is in project root (not in backend/)
- Check: File should be at `Agentic_V2.0/Dockerfile` (already correct)

**"Directory not found: backend"**
- Solution: Make sure backend/ folder exists in repo
- Check: `git ls-files | grep backend/`

**"Module not found"**
- Solution: Check requirements.txt is complete
- Test locally: `docker build -t test .`

---

## 🧪 Test Locally (Optional)

Before deploying, test Docker build locally:

```bash
# Build Docker image
docker build -t agentic-hiring .

# Run container (test)
docker run -p 8000:10000 \
  -e DATABASE_URL="postgresql://..." \
  -e HF_API_KEY="hf_..." \
  -e SIMILARITY_THRESHOLD="0.90" \
  agentic-hiring

# Test health check
curl http://localhost:8000/health
```

---

## ✅ Deployment Checklist

- [ ] Dockerfile created in project root
- [ ] .dockerignore created
- [ ] render.yaml updated to use Docker
- [ ] Branch is set to `main`
- [ ] All files pushed to GitHub
- [ ] Old failed service deleted in Render (if any)
- [ ] Blueprint created in Render
- [ ] HF_API_KEY environment variable added
- [ ] Deployment started
- [ ] Health check passes

---

## 📞 Still Having Issues?

1. **Share Render logs**: Copy error from Render dashboard "Logs" tab
2. **Verify branch**: `git branch --show-current`
3. **Check files**: `git ls-files | head -20`

---

## 🎯 Expected Result

After successful deployment:
```
✅ Build completed
✅ Docker image created
✅ Container started
✅ Health check passed: /health
✅ Service live at: https://agentic-hiring-backend.onrender.com
```

---

**Ready to deploy? Follow the steps above!** 🚀
