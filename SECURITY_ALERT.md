# 🚨 SECURITY ALERT - API Token Exposed

## ⚠️ IMMEDIATE ACTION REQUIRED

Your HuggingFace API token **`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`** was found in GitHub commits.

---

## 🔴 What Happened

The token was accidentally committed in these files:
- `.env.example`
- `DEPLOYMENT.md`
- `QUICK_DEPLOY.md`
- `DEPLOYMENT_FIX.md`

GitHub's secret scanning detected this and sent you a warning.

---

## ✅ Steps to Fix (Do This NOW)

### Step 1: Revoke the Compromised Token

1. Go to [HuggingFace Settings → Tokens](https://huggingface.co/settings/tokens)
2. Find token: `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`
3. Click **"Revoke"** or **"Delete"**

### Step 2: Generate a New Token

1. On same page, click **"New token"**
2. Name it: `Agentic_Hiring_Platform`
3. Select permissions: **Read** (for inference API)
4. Click **"Generate token"**
5. **Copy the new token** (it starts with `hf_...`)

### Step 3: Update Local Environment

```bash
# Edit your local .env file
cd C:\Users\Lenovo\OneDrive\Desktop\Agentic_Hiring_V2.0\backend

# Update with NEW token
# HF_API_KEY=hf_NEW_TOKEN_HERE
```

**IMPORTANT**: Do NOT commit the new token anywhere!

### Step 4: Update Render Dashboard

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Select your service: **agentic-hiring-backend**
3. Go to **"Environment"** tab
4. Find `HF_API_KEY`
5. Click **"Edit"**
6. Paste your **NEW token**
7. Click **"Save Changes"**
8. Service will automatically redeploy

### Step 5: Commit Token Removal

```bash
cd C:\Users\Lenovo\OneDrive\Desktop\Agentic_Hiring_V2.0

git add .
git commit -m "Security: Remove exposed HuggingFace API token"
git push origin main
```

This removes the token from all documentation files.

---

## 🔒 Prevention for Future

### What NOT to Do
❌ Never put real tokens in `.env.example`  
❌ Never put real tokens in documentation files  
❌ Never commit `.env` file to git  

### What TO Do
✅ Use placeholders in `.env.example`: `hf_YOUR_TOKEN_HERE`  
✅ Keep real tokens only in `.env` (which is .gitignored)  
✅ Use environment variables in CI/CD (Render, GitHub Actions)  
✅ Rotate tokens periodically  

---

## 📋 Verification Checklist

After completing all steps:

- [ ] Old token revoked in HuggingFace
- [ ] New token generated
- [ ] Local `.env` updated with new token
- [ ] Render environment variable updated with new token
- [ ] Changes committed to GitHub
- [ ] Verified no tokens in documentation files
- [ ] Confirmed `.env` is in `.gitignore`

---

## 🔍 Check for Other Exposed Secrets

```bash
# Check for any secrets in committed files
git log --all -S "hf_" --source --oneline

# Check current files
grep -r "hf_" . --exclude-dir=.git --exclude-dir=node_modules
```

---

## ❓ FAQ

**Q: Is my account compromised?**  
A: The token only allows API access to HuggingFace models. Revoke it immediately to prevent unauthorized usage.

**Q: Will my app stop working?**  
A: Yes, temporarily. Once you update Render with the new token, it will work again.

**Q: Can I reuse the old token?**  
A: **NO!** It's public on GitHub. Always use a fresh token.

**Q: How do I check if someone used my token?**  
A: Check [HuggingFace Usage](https://huggingface.co/settings/tokens) for unusual activity.

---

## 📞 Need Help?

- HuggingFace Support: https://huggingface.co/support
- GitHub Security Alerts: https://github.com/settings/security
- Render Support: https://render.com/docs

---

**⏱️ DO THIS NOW** - The longer a token is exposed, the higher the risk!

---

## ✅ After Fixing

Once you've:
1. ✅ Revoked old token
2. ✅ Generated new token
3. ✅ Updated Render
4. ✅ Pushed secure code

You can delete this file:
```bash
git rm SECURITY_ALERT.md
git commit -m "Security: Issue resolved"
git push
```

---

**Last Updated**: February 12, 2026  
**Status**: 🔴 URGENT - Action Required
