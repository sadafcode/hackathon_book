# Railway Deployment Quick Fix

## The Error You're Seeing

```
pip install -r requirements.txt
sh: 1: pip: not found
ERROR: failed to build: failed to solve: process "sh -c pip install -r requirements.txt" did not complete successfully: exit code: 127
```

## Why This Happens

Railway is trying to deploy from the **root directory** of your repository instead of the `backend/` folder. It can't find `requirements.txt` or Python because it's looking in the wrong place.

## The Fix (5 Steps)

### Step 1: Set Root Directory in Railway

1. Go to your Railway dashboard
2. Click on your service/project
3. Click **Settings** tab
4. Scroll down to **Service Settings** section
5. Find **Root Directory** field
6. Type: `backend`
7. Click **Save**

### Step 2: Trigger Redeploy

Railway should automatically redeploy. If not:
- Go to **Deployments** tab
- Click **Deploy** button

### Step 3: Watch the Build Logs

- Stay on the Deployments page
- Watch the logs in real-time
- You should see: `pip install -r requirements.txt` succeed this time

### Step 4: Set Environment Variables

Once the build succeeds, make sure you have these environment variables set in **Settings → Variables**:

**Required:**
- `OPENAI_API_KEY` - Your OpenAI API key
- `QDRANT_URL` - Your Qdrant vector database URL
- `QDRANT_API_KEY` - Your Qdrant API key
- `POSTGRES_HOST` - PostgreSQL host
- `POSTGRES_PORT` - Usually `5432`
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database username
- `POSTGRES_PASSWORD` - Database password

**Optional (Railway sets automatically):**
- `PORT` - Railway will set this automatically

### Step 5: Get Your Backend URL

Once deployed successfully:
1. Go to **Settings** tab
2. Under **Domains** section
3. Copy the Railway-provided URL (looks like `https://yourapp.up.railway.app`)
4. You'll need this URL for the frontend configuration

## Next: Connect Frontend

After backend is deployed, configure GitHub to use this backend URL:

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Create new secret:
   - Name: `CHATBOT_API_URL`
   - Value: Your Railway URL (e.g., `https://yourapp.up.railway.app`)

4. Push your changes:
   ```bash
   git add .
   git commit -m "Fix Railway deployment configuration"
   git push origin main
   ```

## Verification

### Test Backend Health
```bash
curl https://yourapp.up.railway.app/health
```

Should return:
```json
{"status": "healthy"}
```

### Test Chatbot
Once GitHub Pages redeploys with the new backend URL, open your site and try the chatbot!

## Still Having Issues?

Check the full `DEPLOYMENT.md` file for comprehensive troubleshooting.

Common issues:
- Missing environment variables → Add them in Railway Settings → Variables
- CORS errors → Make sure `https://sadafcode.github.io` is in `backend/main.py` CORS origins (already added!)
- Database connection errors → Verify PostgreSQL and Qdrant credentials
