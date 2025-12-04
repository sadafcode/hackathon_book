# Railway Deployment Checklist

**Date:** 2025-12-04
**Status:** ✅ Ready to Deploy
**GitHub:** ✅ All changes pushed

---

## Pre-Deployment Verification

✅ **Code Changes Pushed to GitHub**
- 5 commits successfully pushed
- All Railway configuration files included
- .gitignore properly configured (backend/.env is protected)

✅ **Backend Verified Locally**
- All tests passed (see LOCAL_TEST_RESULTS.md)
- 98 chunks ingested in vector database
- RAG pipeline working (relevance scores 0.56-0.77)
- Response quality: Excellent

✅ **Configuration Files Present**
- ✅ backend/Procfile
- ✅ backend/railway.json
- ✅ backend/nixpacks.toml
- ✅ backend/runtime.txt
- ✅ backend/requirements.txt
- ✅ backend/.env.example (template for Railway env vars)

---

## Step-by-Step Deployment Guide

### PHASE 1: Deploy Backend to Railway (10 minutes)

#### Step 1: Login to Railway
```
1. Go to: https://railway.app
2. Sign in with your GitHub account
3. Authorize Railway to access your repositories
```

#### Step 2: Create New Project
```
1. Click "New Project" button
2. Select "Deploy from GitHub repo"
3. Search for "hackathon_book"
4. Click on "sadafcode/hackathon_book"
5. Railway will start analyzing the repository
```

#### Step 3: Configure Root Directory ⚠️ CRITICAL!
```
This is THE MOST IMPORTANT step. Without this, deployment will fail!

1. After Railway creates the service, click on it
2. Go to "Settings" tab
3. Scroll down to "Service Settings" section
4. Find "Root Directory" field
5. Type: backend
6. Click "Save"

⚠️ DO NOT SKIP THIS STEP! The error "pip: not found" happens if you skip this.
```

#### Step 4: Set Environment Variables
```
1. Still in the service, click "Variables" tab
2. Click "Add Variable" for each of these:

Required Variables:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Variable: GOOGLE_API_KEY
Value: [Your Google Gemini API key]
Source: https://makersuite.google.com/app/apikey

Variable: QDRANT_HOST
Value: [Your Qdrant cluster URL]
Example: https://xyz-abc-123.qdrant.io:6333

Variable: QDRANT_API_KEY
Value: [Your Qdrant API key]
Source: Qdrant Cloud dashboard

Variable: QDRANT_COLLECTION_NAME
Value: chatbot_knowledge
(Or whatever collection name you used during ingestion)

Variable: DATABASE_URL
Value: [Your PostgreSQL connection string]
Format: postgresql+asyncpg://user:password@host:port/database
Note: Railway provides PostgreSQL - see PostgreSQL Setup section below

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. After adding all variables, click "Deploy" if not auto-deployed
```

#### Step 5: PostgreSQL Setup (If using Railway PostgreSQL)
```
Option A: Add PostgreSQL from Railway:
1. In your Railway project, click "New" → "Database" → "PostgreSQL"
2. Railway will create a PostgreSQL instance
3. Go to the PostgreSQL service → "Variables" tab
4. Copy the "DATABASE_URL" value
5. In your backend service → "Variables" → Paste DATABASE_URL

Option B: Use External PostgreSQL:
1. Use your existing PostgreSQL connection string
2. Format: postgresql+asyncpg://user:password@host:port/database
3. Add to backend service variables
```

#### Step 6: Monitor Deployment
```
1. Go to "Deployments" tab
2. Click on the latest deployment
3. Watch the logs in real-time
4. Look for these success indicators:

   ✅ "pip install -r requirements.txt" succeeds
   ✅ "uvicorn main:app --host 0.0.0.0 --port $PORT" starts
   ✅ "Initializing database and Qdrant collection..."
   ✅ "Database and Qdrant collection initialized."
   ✅ "Application startup complete."
   ✅ Deployment status shows "Active"

If you see errors, check the Troubleshooting section below.
```

#### Step 7: Get Your Backend URL
```
1. Go to "Settings" tab
2. Scroll to "Domains" section
3. Copy the Railway-provided URL
   Example: https://hackathon-book-production.up.railway.app

4. Test the health endpoint:
   curl https://your-app.railway.app/health

   Should return: {"status":"healthy"}
```

#### Step 8: Test Backend on Railway
```bash
# Test health endpoint
curl https://your-app.railway.app/health

# Test chat endpoint
curl -X POST https://your-app.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is physical AI?"}'

# Should return a response with source_urls
```

---

### PHASE 2: Configure GitHub Pages (5 minutes)

#### Step 9: Add GitHub Secret
```
1. Go to: https://github.com/sadafcode/hackathon_book
2. Click "Settings" tab
3. In left sidebar, click "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Add secret:
   Name: CHATBOT_API_URL
   Value: https://your-app.railway.app
   (Use the Railway URL from Step 7)
6. Click "Add secret"
```

#### Step 10: Enable GitHub Pages
```
1. Still in repository Settings
2. Click "Pages" in left sidebar
3. Under "Source", select "GitHub Actions"
4. Click "Save"
```

#### Step 11: Trigger Deployment
```
Your code is already pushed, so GitHub Actions should already be running!

1. Go to "Actions" tab in your repository
2. Look for "Deploy to GitHub Pages" workflow
3. If not running, click "Run workflow" → "Run workflow"
4. Watch the deployment progress
5. Wait for green checkmark (usually 2-3 minutes)
```

#### Step 12: Verify Frontend Deployment
```
1. After GitHub Actions completes:
2. Go to: https://sadafcode.github.io/hackathon_book/
3. Wait for page to load
4. Look for the "Chat" button (bottom right corner)
5. Click it to open the chatbot
```

---

### PHASE 3: End-to-End Testing (5 minutes)

#### Step 13: Test Chatbot on Production
```
1. Open: https://sadafcode.github.io/hackathon_book/
2. Click the "Chat" button
3. Type a question: "What is physical AI?"
4. Press Enter
5. Wait for response (should appear in 5-10 seconds)

Expected Results:
✅ Chatbot opens successfully
✅ Question is accepted
✅ Response appears with relevant information
✅ Source URLs are shown at bottom
✅ No CORS errors in browser console (F12)

Test Additional Queries:
- "What are humanoid robots?"
- "Explain embodied intelligence"
- Select text on the page, then ask "Summarize this"
```

#### Step 14: Check Browser Console
```
1. Press F12 to open Developer Tools
2. Go to "Console" tab
3. Look for any errors (should be none)

Common Issues to Check:
❌ CORS errors → Check backend/main.py CORS origins
❌ Failed to fetch → Check CHATBOT_API_URL secret
❌ 500 errors → Check Railway backend logs
```

---

## Environment Variables Reference

### Backend (Railway)

| Variable | Required | Example | Where to Get |
|----------|----------|---------|--------------|
| `GOOGLE_API_KEY` | ✅ Yes | `AIza...` | https://makersuite.google.com/app/apikey |
| `QDRANT_HOST` | ✅ Yes | `https://xyz.qdrant.io:6333` | Qdrant Cloud dashboard |
| `QDRANT_API_KEY` | ✅ Yes | `abc123...` | Qdrant Cloud dashboard |
| `QDRANT_COLLECTION_NAME` | ⚠️ Optional | `chatbot_knowledge` | Defaults to "chatbot_knowledge" |
| `DATABASE_URL` | ✅ Yes | `postgresql+asyncpg://...` | Railway PostgreSQL or your DB |

### Frontend (GitHub Secret)

| Secret | Required | Example | Where to Get |
|--------|----------|---------|--------------|
| `CHATBOT_API_URL` | ✅ Yes | `https://your-app.railway.app` | Railway → Settings → Domains |

---

## Troubleshooting

### Issue 1: "pip: not found" Error

**Symptom:**
```
pip install -r requirements.txt
sh: 1: pip: not found
ERROR: failed to build
```

**Solution:**
1. Go to Railway service → Settings
2. Set **Root Directory** to `backend`
3. Save and redeploy

**Why:** Railway was trying to deploy from project root instead of backend folder.

---

### Issue 2: Deployment Stuck or Failing

**Symptoms:**
- Build process hangs
- Multiple failed deployments
- Random errors

**Solution:**
1. Check Railway logs for specific error messages
2. Verify ALL environment variables are set correctly
3. Try "Restart" from Railway dashboard
4. If still failing, create new service and configure again

---

### Issue 3: Chatbot Not Responding

**Symptoms:**
- Chatbot opens but shows "Failed to get response"
- Browser console shows CORS errors
- Network errors

**Solution:**

**A. CORS Error:**
```
1. Check backend/main.py line 13-17
2. Verify https://sadafcode.github.io is in origins list
3. Redeploy backend if needed
```

**B. Wrong Backend URL:**
```
1. GitHub → Settings → Secrets
2. Check CHATBOT_API_URL value
3. Should match Railway domain EXACTLY
4. No trailing slashes!
```

**C. Backend Down:**
```
1. Test health endpoint: curl https://your-app.railway.app/health
2. If fails, check Railway logs
3. Check if backend service is running
```

---

### Issue 4: "No relevant information" Responses

**Symptom:**
- Chatbot responds but says "couldn't find any relevant information"
- Happens for all queries

**Solution:**
```
Problem: Vector database is empty (ingestion didn't run on Railway)

Fix:
1. Connect to Railway shell (Dashboard → Service → Shell tab)
2. Run: python ingestion.py
3. Wait for completion
4. Test again

Note: For this deployment, you already ran ingestion locally,
      so your data should be in Qdrant already!
```

---

### Issue 5: GitHub Actions Fails

**Symptom:**
- "Deploy to GitHub Pages" workflow fails
- Build errors in Actions tab

**Solution:**
```
1. Check if CHATBOT_API_URL secret is set
2. Verify secret name is exactly: CHATBOT_API_URL
3. Check Actions logs for specific error
4. Try re-running the workflow
```

---

## Post-Deployment Checklist

After successful deployment:

- [ ] Backend health check returns 200 OK
- [ ] Backend chat endpoint responds correctly
- [ ] Frontend loads at https://sadafcode.github.io/hackathon_book/
- [ ] Chatbot button appears on page
- [ ] Chatbot opens when clicked
- [ ] Test query returns relevant answer
- [ ] Source URLs are displayed
- [ ] No CORS errors in browser console
- [ ] Selected text feature works
- [ ] Response time is acceptable (< 10 seconds)

---

## Monitoring & Maintenance

### Railway Monitoring
```
1. Railway Dashboard → Your Service → Metrics
2. Monitor:
   - Request count
   - Response times
   - Error rates
   - Memory usage
   - CPU usage

3. Check logs regularly for errors
```

### GitHub Actions Monitoring
```
1. Repository → Actions tab
2. Monitor deployments
3. Fix any failed workflows
4. Keep an eye on build times
```

### Cost Monitoring
```
Railway Free Tier: $5/month credit

To monitor usage:
1. Railway → Account Settings → Billing
2. Check usage dashboard
3. Set up alerts for approaching limit
```

---

## Quick Reference Commands

### Test Backend Health
```bash
curl https://your-app.railway.app/health
```

### Test Chat Endpoint
```bash
curl -X POST https://your-app.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'
```

### View Railway Logs
```bash
# Install Railway CLI (optional)
npm install -g @railway/cli

# Login
railway login

# View logs
railway logs
```

### Redeploy Backend
```
Railway Dashboard → Service → Deployments → Click "Deploy"
```

### Redeploy Frontend
```bash
# Trigger GitHub Actions manually:
# GitHub → Actions → Deploy to GitHub Pages → Run workflow
```

---

## Success Indicators

You'll know deployment is successful when:

✅ Railway shows "Active" status with green indicator
✅ Health endpoint returns {"status":"healthy"}
✅ Chat endpoint returns valid responses with source_urls
✅ Frontend loads without errors
✅ Chatbot widget appears and responds
✅ No CORS errors in browser console
✅ Responses are relevant and include source attribution
✅ Response times are under 10 seconds

---

## Next Steps After Deployment

1. **Share Your Chatbot:**
   - URL: https://sadafcode.github.io/hackathon_book/
   - Share with team/users for feedback

2. **Monitor Performance:**
   - Watch Railway logs for errors
   - Check response times
   - Monitor user feedback

3. **Iterate & Improve:**
   - Add more content to docs
   - Re-run ingestion.py when content changes
   - Tune chunk size for better results
   - Adjust search limit (currently 5 chunks)

4. **Optional Enhancements:**
   - Add user authentication
   - Implement rate limiting
   - Add analytics/tracking
   - Improve UI/UX
   - Add more AI features

---

## Support Resources

- **Railway Documentation:** https://docs.railway.app/
- **Railway Discord:** https://discord.gg/railway
- **GitHub Actions Docs:** https://docs.github.com/actions
- **Qdrant Docs:** https://qdrant.tech/documentation/
- **Google Gemini API:** https://ai.google.dev/docs

---

## Deployment Timeline Estimate

| Phase | Task | Time |
|-------|------|------|
| **Phase 1** | Railway Backend Setup | 10 minutes |
| **Phase 2** | GitHub Pages Config | 5 minutes |
| **Phase 3** | Testing & Verification | 5 minutes |
| **Total** | Complete Deployment | **20 minutes** |

---

## Ready to Deploy? Let's Go! 🚀

Start with **PHASE 1: Step 1** and follow each step carefully.

Good luck with your deployment!

---

**Last Updated:** 2025-12-04
**Version:** 1.0
**Author:** Claude Code
**Status:** Production Ready ✅
