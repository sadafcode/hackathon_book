# Deployment Guide

This guide explains how to deploy the Docusaurus frontend to GitHub Pages and the FastAPI backend to Railway.

## Prerequisites

- GitHub account with repository access
- Railway account (https://railway.app)
- Environment variables configured

## Backend Deployment (Railway)

### Step 1: Prepare Your Backend

The backend is already configured with the necessary files:
- `backend/Procfile` - Tells Railway how to start the app
- `backend/railway.json` - Railway-specific configuration
- `backend/runtime.txt` - Python version specification
- `backend/requirements.txt` - Python dependencies

### Step 2: Deploy to Railway

1. **Login to Railway**
   - Go to https://railway.app
   - Sign in with your GitHub account

2. **Create a New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `hackathon_book` repository
   - Railway will detect the backend automatically

3. **CRITICAL: Configure Root Directory**
   - Click on your service (it will show up after selecting the repo)
   - Go to **Settings** tab
   - Scroll down to **Service Settings**
   - Set **Root Directory** to `backend`
   - Click **Save**
   - **This is the most important step!** Without this, Railway will try to deploy from the root directory and fail.

4. **Set Environment Variables**

   In Railway project settings, add these environment variables:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   POSTGRES_HOST=your_postgres_host
   POSTGRES_PORT=5432
   POSTGRES_DB=your_database_name
   POSTGRES_USER=your_database_user
   POSTGRES_PASSWORD=your_database_password
   PORT=8000
   ```

5. **Deploy**
   - Railway will automatically build and deploy your backend
   - Once deployed, you'll get a URL like: `https://your-app.railway.app`
   - Copy this URL - you'll need it for the frontend

### Step 3: Test Your Backend

Test the health endpoint:
```bash
curl https://your-app.railway.app/health
```

Expected response:
```json
{"status": "healthy"}
```

## Frontend Deployment (GitHub Pages)

### Step 1: Configure Backend URL in GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add:
   - Name: `CHATBOT_API_URL`
   - Value: `https://your-app.railway.app` (your Railway backend URL)

### Step 2: Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. Save the settings

### Step 3: Deploy

The GitHub Actions workflow (`.github/workflows/deploy.yml`) will automatically:
1. Build the Docusaurus site with the backend URL
2. Deploy to GitHub Pages

To trigger deployment:
```bash
git add .
git commit -m "Configure deployment"
git push origin main
```

### Step 4: Verify Deployment

Your site will be available at:
```
https://sadafcode.github.io/hackathon_book/
```

## Troubleshooting

### Backend Issues

1. **"pip: not found" or "failed to build" Error**

   **Problem:** Railway is trying to install dependencies from the wrong directory

   **Solution:**
   - Go to your Railway project
   - Click on your service
   - Go to **Settings** tab
   - Scroll to **Service Settings**
   - Set **Root Directory** to `backend` (this is CRITICAL!)
   - Save and redeploy

   This ensures Railway looks for `requirements.txt` in the `backend/` folder, not the root.

2. **Railway Build Fails with Other Errors**
   - Check logs in Railway dashboard (Deployments → Click on failed deployment → View logs)
   - Verify all environment variables are set in Settings → Variables
   - Ensure `backend/requirements.txt` has all dependencies
   - Check that `backend/nixpacks.toml` exists and is properly configured

3. **CORS Errors (Frontend can't connect to backend)**
   - Verify GitHub Pages URL is in `backend/main.py` CORS origins
   - Current allowed origin: `https://sadafcode.github.io`
   - If you changed your GitHub username or repo name, update the CORS origins accordingly

4. **Database Connection Errors**
   - Verify PostgreSQL credentials in Railway environment variables
   - Check if Qdrant is accessible from Railway
   - Ensure database is running and accessible (Railway provides PostgreSQL as a service)

### Frontend Issues

1. **Chatbot Not Connecting**
   - Check if `CHATBOT_API_URL` secret is set in GitHub
   - Verify the backend URL is correct
   - Open browser console to see error messages

2. **GitHub Actions Fails**
   - Check the Actions tab for error logs
   - Verify Node.js version compatibility (should be 20)

## Local Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
npm install
npm start
```

The frontend will run on `http://localhost:3000` and connect to `http://localhost:8000` for the backend.

## Environment Variables Reference

### Required for Backend (Railway)

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for embeddings | `sk-...` |
| `QDRANT_URL` | Qdrant vector database URL | `https://xyz.qdrant.io` |
| `QDRANT_API_KEY` | Qdrant API key | `your-key` |
| `POSTGRES_HOST` | PostgreSQL host | `postgres.railway.internal` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_DB` | Database name | `railway` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `your-password` |
| `PORT` | Port for FastAPI (Railway sets this) | `8000` |

### Required for Frontend (GitHub Secrets)

| Secret | Description | Example |
|--------|-------------|---------|
| `CHATBOT_API_URL` | Backend API URL | `https://your-app.railway.app` |

## Updating Deployments

### Update Backend
```bash
cd backend
# Make your changes
git add .
git commit -m "Update backend"
git push origin main
```
Railway will automatically redeploy.

### Update Frontend
```bash
# Make your changes
git add .
git commit -m "Update frontend"
git push origin main
```
GitHub Actions will automatically rebuild and redeploy.

## Cost Considerations

- **Railway**: Free tier includes $5/month credit, then pay-as-you-go
- **GitHub Pages**: Free for public repositories
- **Qdrant**: Check their pricing (may have free tier)
- **PostgreSQL on Railway**: Included in Railway usage

## Support

If you encounter issues:
1. Check Railway logs: Railway Dashboard → Your Project → Deployments → Logs
2. Check GitHub Actions logs: GitHub → Actions tab
3. Check browser console for frontend errors
