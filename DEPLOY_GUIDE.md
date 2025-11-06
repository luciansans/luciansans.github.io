# 🚀 Deployment Guide - Doctor Appointment System

Complete guide to deploy your application with frontend on GitHub Pages and backend on Render.

---

## Quick Overview

- **Frontend**: GitHub Pages (https://luciansans.github.io)
- **Backend**: Render (https://your-app.onrender.com)
- **Database**: SQLite (free) or PostgreSQL (recommended)

---

## Step 1: Deploy Backend to Render

### 1.1 Create Render Account
1. Go to https://render.com and sign up
2. Verify your email

### 1.2 Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `luciansans.github.io`
3. Configure:
   - **Name**: `clinic-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

### 1.3 Set Environment Variables
Click "Advanced" and add these environment variables:

```
DATABASE_URL=sqlite:///./clinic.db
SECRET_KEY=<click Generate button>
CORS_ORIGINS=https://luciansans.github.io
DEBUG=False
APP_NAME=Doctor Appointment System
APP_VERSION=1.0.0
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 1.4 Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. **Note your backend URL**: `https://__________.onrender.com`

### 1.5 Test Backend
Visit these URLs:
- `https://your-app.onrender.com/` - API info
- `https://your-app.onrender.com/api/health` - Health check
- `https://your-app.onrender.com/docs` - API documentation

---

## Step 2: Update Frontend Configuration

### 2.1 Update API URL
1. Open `js/config.js`
2. Update line 8:
```javascript
PRODUCTION_API_URL: 'https://your-actual-app.onrender.com/api',
```

### 2.2 Commit Changes
```bash
git add js/config.js
git commit -m "Update production API URL"
git push origin main
```

---

## Step 3: Deploy Frontend to GitHub Pages

### 3.1 Enable GitHub Pages
1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**

### 3.2 Wait for Deployment
- GitHub Pages deploys in 1-2 minutes
- Visit: `https://luciansans.github.io`

---

## Step 4: Test Your Application

### 4.1 Test Registration
1. Visit `https://luciansans.github.io`
2. Click "Register"
3. Create a test account
4. Should see success message

### 4.2 Test Login
1. Login with your credentials
2. Username should appear in navigation

### 4.3 Test Features
- View doctors list
- Book an appointment
- Check queue status

---

## Troubleshooting

### ❌ Frontend can't connect to backend
**Fix:**
1. Check `js/config.js` has correct backend URL
2. Verify `CORS_ORIGINS` in Render includes `https://luciansans.github.io`
3. Check backend is running in Render dashboard

### ❌ Backend not starting
**Fix:**
1. Check Render logs for errors
2. Verify all environment variables are set
3. Ensure `requirements.txt` is complete

### ❌ "Service Unavailable" on first request
**This is normal!**
- Render free tier spins down after 15 minutes
- First request takes 30-60 seconds to wake up

---

## Project Structure

```
luciansans.github.io/
├── backend/              # Backend API (deploy to Render)
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Configuration
│   │   └── models/      # Database models
│   ├── requirements.txt
│   ├── render.yaml
│   └── .env.example
├── css/                 # Frontend styles
├── js/                  # Frontend JavaScript
│   ├── config.js       # API configuration (UPDATE THIS!)
│   ├── main.js
│   ├── appointments.js
│   └── queue.js
├── index.html          # Main page
└── DEPLOY_GUIDE.md     # This file
```

---

## Important Files

### Backend Files:
- `backend/render.yaml` - Render deployment config
- `backend/.env.example` - Environment variables template
- `backend/app/core/config.py` - Application configuration

### Frontend Files:
- `js/config.js` - **UPDATE THIS with your Render URL**
- `index.html` - Main application page
- `js/main.js` - Main JavaScript logic

---

## Upgrade to PostgreSQL (Recommended)

For production, use PostgreSQL instead of SQLite:

1. In Render Dashboard: **New +** → **PostgreSQL**
2. Name: `clinic-db`
3. Copy the **Internal Database URL**
4. Update `DATABASE_URL` in your web service
5. Add to `requirements.txt`: `psycopg2-binary==2.9.9`
6. Redeploy

---

## Security Checklist

- ✅ SECRET_KEY is randomly generated (use Render's Generate button)
- ✅ DEBUG is False in production
- ✅ CORS_ORIGINS only includes your domain
- ✅ Never commit `.env` files to Git
- ✅ HTTPS is enabled (automatic)

---

## Support

### API Endpoints
- **Health**: `/api/health`
- **Docs**: `/docs`
- **Auth**: `/api/auth/login`, `/api/auth/register`
- **Doctors**: `/api/doctors/`
- **Appointments**: `/api/appointments/`
- **Queue**: `/api/queue/status/{doctor_id}`

### Resources
- Render Docs: https://render.com/docs
- GitHub Pages: https://docs.github.com/pages
- FastAPI: https://fastapi.tiangolo.com/

---

## Success! 🎉

Your application is now live:
- **Frontend**: https://luciansans.github.io
- **Backend**: https://your-app.onrender.com
- **API Docs**: https://your-app.onrender.com/docs

---

## Quick Commands

```bash
# Test backend locally
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Test frontend locally
python -m http.server 8080

# Commit and push changes
git add .
git commit -m "Deploy application"
git push origin main
```

---

**Deployment Date**: _______________
**Backend URL**: _______________
**Notes**: _______________