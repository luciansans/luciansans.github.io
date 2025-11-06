# Deployment Guide: Doctor Appointment System

This guide will help you deploy your application with the frontend on GitHub Pages and the backend on Render.

## Architecture Overview

- **Frontend**: Static HTML/CSS/JS hosted on GitHub Pages (https://luciansans.github.io)
- **Backend**: FastAPI Python application hosted on Render
- **Database**: SQLite (for free tier) or PostgreSQL (recommended for production)

## Prerequisites

1. GitHub account with repository: `luciansans.github.io`
2. Render account (free tier available at https://render.com)
3. Git installed on your local machine

---

## Part 1: Deploy Backend to Render

### Step 1: Prepare Your Repository

1. Ensure your backend code is in the `backend/` directory
2. Verify these files exist:
   - `backend/requirements.txt`
   - `backend/render.yaml`
   - `backend/.env.example`
   - `backend/app/main.py`

### Step 2: Create Render Web Service

#### Option A: Using render.yaml (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Click **"Apply"**

#### Option B: Manual Setup

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `clinic-backend` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

### Step 3: Configure Environment Variables

In Render dashboard, go to your service → **Environment** tab and add:

```
DATABASE_URL=sqlite:///./clinic.db
SECRET_KEY=<click "Generate" for a secure random key>
CORS_ORIGINS=https://luciansans.github.io
DEBUG=False
APP_NAME=Doctor Appointment System
APP_VERSION=1.0.0
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Important Notes:**
- For production, consider using PostgreSQL instead of SQLite
- Never commit your actual `.env` file with secrets to GitHub
- Use Render's "Generate" button for SECRET_KEY

### Step 4: Deploy

1. Click **"Create Web Service"** or **"Manual Deploy"**
2. Wait for deployment to complete (5-10 minutes)
3. Note your backend URL: `https://your-app-name.onrender.com`

### Step 5: Test Backend

Visit these URLs to verify deployment:
- `https://your-app-name.onrender.com/` - Should show API info
- `https://your-app-name.onrender.com/api/health` - Should return health status
- `https://your-app-name.onrender.com/docs` - FastAPI interactive documentation

---

## Part 2: Deploy Frontend to GitHub Pages

### Step 1: Update Frontend Configuration

1. Open `frontend/js/config.js`
2. Update the `PRODUCTION_API_URL` with your Render backend URL:

```javascript
PRODUCTION_API_URL: 'https://your-app-name.onrender.com/api',
```

### Step 2: Prepare GitHub Repository

1. Ensure your frontend files are in the `frontend/` directory
2. Copy frontend files to root for GitHub Pages:

```bash
# From your repository root
cp -r frontend/* .
```

Or manually copy these files to the root:
- `frontend/index.html` → `index.html`
- `frontend/css/` → `css/`
- `frontend/js/` → `js/`

### Step 3: Enable GitHub Pages

1. Go to your GitHub repository settings
2. Navigate to **Pages** section
3. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**

### Step 4: Commit and Push

```bash
git add .
git commit -m "Deploy frontend and backend configuration"
git push origin main
```

### Step 5: Wait for Deployment

- GitHub Pages typically deploys in 1-2 minutes
- Visit: `https://luciansans.github.io`

---

## Part 3: Verify Full Integration

### Test the Complete Flow

1. **Visit Frontend**: `https://luciansans.github.io`
2. **Register**: Create a new account
3. **Login**: Use your credentials
4. **View Doctors**: Check if doctors list loads
5. **Book Appointment**: Try booking an appointment
6. **Check Queue**: View queue status

### Troubleshooting

#### Frontend Can't Connect to Backend

**Symptoms**: CORS errors, network errors in browser console

**Solutions**:
1. Verify `CORS_ORIGINS` in Render includes your GitHub Pages URL
2. Check `config.js` has correct backend URL
3. Ensure backend is running (check Render logs)
4. Clear browser cache and reload

#### Backend Not Starting

**Symptoms**: Render shows "Deploy failed" or service crashes

**Solutions**:
1. Check Render logs for error messages
2. Verify `requirements.txt` has all dependencies
3. Ensure `DATABASE_URL` is set correctly
4. Check Python version compatibility

#### Database Issues

**Symptoms**: 500 errors when creating users/appointments

**Solutions**:
1. For SQLite: Ensure write permissions (may need PostgreSQL on Render)
2. Check database initialization in logs
3. Consider upgrading to PostgreSQL for production

---

## Part 4: Upgrade to PostgreSQL (Recommended)

### Why PostgreSQL?

- SQLite has limitations on Render's ephemeral filesystem
- PostgreSQL is more reliable for production
- Free tier available on Render

### Steps to Upgrade

1. **Create PostgreSQL Database on Render**:
   - Dashboard → **New +** → **PostgreSQL**
   - Name: `clinic-db`
   - Region: Same as your web service
   - Click **Create Database**

2. **Update requirements.txt**:
   ```
   psycopg2-binary==2.9.9
   ```

3. **Update Environment Variable**:
   - Copy the **Internal Database URL** from PostgreSQL dashboard
   - Update `DATABASE_URL` in your web service environment variables

4. **Redeploy**:
   - Render will automatically redeploy with new database

---

## Part 5: Ongoing Maintenance

### Monitoring

- **Render Dashboard**: Monitor service health, logs, and metrics
- **GitHub Actions**: Set up CI/CD for automated deployments
- **Error Tracking**: Consider integrating Sentry or similar

### Updates

1. Make changes locally
2. Test thoroughly
3. Commit and push to GitHub
4. Render auto-deploys backend (if enabled)
5. GitHub Pages auto-deploys frontend

### Backup

- **Database**: Use Render's backup features or pg_dump
- **Code**: Always maintain in Git repository

---

## Security Checklist

- [ ] SECRET_KEY is randomly generated and secure
- [ ] DEBUG is set to False in production
- [ ] CORS_ORIGINS only includes your domains
- [ ] Database credentials are not in code
- [ ] HTTPS is enabled (automatic on Render and GitHub Pages)
- [ ] Input validation is implemented
- [ ] SQL injection protection (using SQLAlchemy ORM)

---

## Cost Considerations

### Free Tier Limitations

**Render Free Tier**:
- Service spins down after 15 minutes of inactivity
- 750 hours/month (enough for one service)
- First request after spin-down takes 30-60 seconds

**GitHub Pages**:
- Completely free for public repositories
- 100GB bandwidth/month
- 1GB storage

### Upgrade Options

If you need better performance:
- Render Starter: $7/month (always-on, better resources)
- PostgreSQL: $7/month (persistent database)

---

## Support and Resources

- **Render Documentation**: https://render.com/docs
- **GitHub Pages**: https://docs.github.com/pages
- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/

---

## Quick Reference Commands

```bash
# Test backend locally
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Test frontend locally
cd frontend
python -m http.server 8080

# Check backend logs on Render
# Go to Render Dashboard → Your Service → Logs

# Force redeploy on Render
# Dashboard → Your Service → Manual Deploy → Deploy latest commit
```

---

## Congratulations! 🎉

Your Doctor Appointment System is now live:
- Frontend: https://luciansans.github.io
- Backend: https://your-app-name.onrender.com
- API Docs: https://your-app-name.onrender.com/docs