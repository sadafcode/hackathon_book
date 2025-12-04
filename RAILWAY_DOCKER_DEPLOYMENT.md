# Railway Docker Deployment Guide

**Solution for Build Timeout Issues**

Since Railway's build times out when installing PyTorch and sentence-transformers, we'll use Docker to build the image locally and deploy to Railway.

---

## Why Docker?

✅ **Solves timeout issues** - Build on your machine, not Railway's
✅ **Full control** - Pre-build heavy dependencies locally
✅ **Faster deploys** - Push pre-built image to Railway
✅ **Works with any dependencies** - No size limits

---

## Prerequisites

1. **Docker Desktop** installed on your machine
   - Download: https://www.docker.com/products/docker-desktop/
   - Make sure Docker is running

2. **Railway CLI** installed
   ```bash
   npm install -g @railway/cli
   ```

3. **Railway Account** logged in
   ```bash
   railway login
   ```

---

## Step-by-Step Deployment

### Step 1: Build Docker Image Locally

```bash
# Navigate to backend directory
cd backend

# Build the Docker image (this will take 5-10 minutes)
docker build -t hackathon-backend:latest .
```

**What happens:**
- Downloads Python 3.11 slim image
- Installs system dependencies (gcc, g++)
- Installs all Python packages including PyTorch
- **This runs on YOUR machine**, not Railway

**Expected output:**
```
[+] Building 450.2s (12/12) FINISHED
=> [1/7] FROM python:3.11-slim
=> [2/7] RUN apt-get update && apt-get install -y gcc g++
=> [3/7] COPY requirements.txt .
=> [4/7] RUN pip install --no-cache-dir -r requirements.txt
=> [5/7] COPY . .
=> exporting to image
Successfully built image
```

---

### Step 2: Test Docker Image Locally

```bash
# Run the container locally to test
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY="your_api_key" \
  -e QDRANT_HOST="your_qdrant_url" \
  -e QDRANT_API_KEY="your_qdrant_key" \
  -e DATABASE_URL="your_db_url" \
  hackathon-backend:latest
```

**Test it:**
```bash
# In another terminal
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is physical AI?"}'
# Should return answer with sources
```

**Stop the container:** Press `Ctrl+C`

---

### Step 3: Deploy to Railway Using Docker

**Option A: Railway CLI (Recommended)**

```bash
# Make sure you're in the backend directory
cd backend

# Link to your Railway project (if not already linked)
railway link

# Deploy using Docker
railway up
```

Railway CLI will:
1. Detect the Dockerfile
2. Build the image (uses your local Docker daemon)
3. Push to Railway's container registry
4. Deploy automatically

**Option B: Railway Dashboard**

1. Go to Railway dashboard
2. Select your service
3. Go to **Settings** → **Deploy**
4. Under "Source", change from "GitHub" to "Docker"
5. Railway will detect the Dockerfile in your repo
6. Click "Deploy"

---

### Step 4: Configure Railway Service

**Set Root Directory:**
```
Settings → Service Settings → Root Directory: backend
```

**Add Environment Variables:**
```
Settings → Variables → Add all your env vars:
- GOOGLE_API_KEY
- QDRANT_HOST
- QDRANT_API_KEY
- QDRANT_COLLECTION_NAME
- DATABASE_URL
```

**Important:** Railway will automatically set the `PORT` environment variable.

---

### Step 5: Verify Deployment

**Check Deployment Status:**
```
1. Go to Railway dashboard → Deployments tab
2. Latest deployment should show "Active"
3. Check logs for "Application startup complete"
```

**Test the deployed backend:**
```bash
# Get your Railway URL from Settings → Domains
export RAILWAY_URL="https://your-app.railway.app"

# Test health
curl $RAILWAY_URL/health

# Test chat
curl -X POST $RAILWAY_URL/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is physical AI?"}'
```

---

## Alternative: Push to Docker Hub (If Railway CLI Issues)

If Railway CLI doesn't work, you can push to Docker Hub:

### Step 1: Create Docker Hub Account
- Go to https://hub.docker.com/
- Sign up (free)

### Step 2: Tag and Push Image

```bash
# Login to Docker Hub
docker login

# Tag your image
docker tag hackathon-backend:latest yourusername/hackathon-backend:latest

# Push to Docker Hub
docker push yourusername/hackathon-backend:latest
```

### Step 3: Deploy from Docker Hub on Railway

1. Railway dashboard → Your service
2. Settings → Source → Change to "Docker Image"
3. Enter: `yourusername/hackathon-backend:latest`
4. Railway will pull and deploy

---

## Dockerfile Explanation

```dockerfile
# Use slim Python image (smaller, faster)
FROM python:3.11-slim

WORKDIR /app

# Install build tools for PyTorch
RUN apt-get update && apt-get install -y gcc g++

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Start the app
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

**Key points:**
- `python:3.11-slim` - Smaller base image (~150MB vs ~1GB)
- `--no-cache-dir` - Reduces image size
- `gcc g++` - Required to build some Python packages
- `${PORT:-8000}` - Uses Railway's PORT or defaults to 8000

---

## Troubleshooting

### Docker Build Fails

**Error:** "Cannot connect to Docker daemon"
**Solution:** Make sure Docker Desktop is running

**Error:** "COPY failed: no source files"
**Solution:** Make sure you're in the `backend/` directory

### Railway Deploy Fails

**Error:** "Failed to pull image"
**Solution:**
1. Check Docker image was built successfully
2. Verify Railway CLI is logged in: `railway whoami`
3. Try `railway up --detach`

### First Request Slow

**Note:** First chat request may take 15-20 seconds to download the embedding model.
This is normal and only happens once. Subsequent requests are fast (~5 seconds).

---

## Performance Expectations

### Build Time (Local):
- First build: 5-10 minutes (downloads PyTorch)
- Subsequent builds: 1-2 minutes (cached layers)

### Image Size:
- Final image: ~3-4 GB (includes PyTorch)
- Railway handles large images fine

### Deployment Time:
- Push to Railway: 2-5 minutes (uploading image)
- First startup: 30-60 seconds
- Health check: Ready in 1 minute

### Runtime Performance:
- Memory usage: ~1-1.5 GB
- Response time: 5-10 seconds
- First request: 15-20 seconds (model download)

---

## Updating Your Deployment

When you make code changes:

```bash
cd backend

# Rebuild image
docker build -t hackathon-backend:latest .

# Test locally (optional)
docker run -p 8000:8000 [env vars] hackathon-backend:latest

# Deploy to Railway
railway up
```

Railway will:
1. Pull your new image
2. Stop old container
3. Start new container
4. Zero-downtime deployment

---

## Cost Considerations

**Docker Desktop:** Free for personal use
**Railway:**
- Starter plan: $5/month + usage
- Docker deployments count towards compute usage
- Large images (3-4GB) are fine

**Estimated Railway Cost:**
- Small traffic: ~$5-10/month
- Medium traffic: ~$10-20/month

---

## Alternative: Multi-stage Docker Build (Advanced)

For even smaller images:

```dockerfile
# Build stage
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

This can reduce image size by 30-50%.

---

## Quick Reference Commands

```bash
# Build
docker build -t hackathon-backend:latest .

# Test locally
docker run -p 8000:8000 [env vars] hackathon-backend:latest

# Deploy to Railway
railway up

# Check Railway logs
railway logs

# Open Railway dashboard
railway open
```

---

## Summary

✅ **Docker solves the build timeout issue**
✅ **Build heavy dependencies locally** (PyTorch, sentence-transformers)
✅ **Deploy pre-built image to Railway**
✅ **Total time: 10-15 minutes** (one-time setup)
✅ **Updates: 5-10 minutes** (rebuild + redeploy)

---

**Ready to deploy? Follow Step 1 to build your Docker image!**

---

**Last Updated:** 2025-12-04
**Status:** Recommended Solution ✅
**Build Time:** 5-10 minutes (one-time)
**Deployment:** Fast and reliable 🚀
