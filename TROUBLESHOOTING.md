# Troubleshooting Guide

## Current Deployment Status

According to your Render dashboard:
- **Latest Commit**: `2b2f170` - "is updated"
- **Deployment Started**: November 6, 2025 at 6:01 PM
- **Previous Deploy**: `9e3af6d` - "waiting on render" (was live at 5:57 PM)

## What Should Happen

The commit `2b2f170` includes ALL previous fixes:
1. ✅ `security.py` - Password truncation fix (from commit `2c57b02`)
2. ✅ `auth.py` - RegisterRequest model with JSON body (from commit `6301bed`)
3. ✅ `main.js` - Updated to send JSON POST request (from commit `6301bed`)
4. ✅ `requirements.txt` - Updated dependencies (from commit `9e3af6d`)

## Step-by-Step Verification

### 1. Wait for Render Deployment to Complete
- Deployments typically take 5-10 minutes
- Check your Render dashboard for "Deploy live for 2b2f170"
- Look for the green "Live" badge

### 2. Check Render Logs
Once deployment is complete, check the logs for:
```
✅ GOOD: "Application startup complete"
✅ GOOD: "Uvicorn running on http://0.0.0.0:10000"
❌ BAD: Any Python errors or "ValueError: password cannot be longer than 72 bytes"
```

### 3. Test the Backend API Directly

Open your browser and test these URLs:

**A. Health Check**
```
https://luciansans-github-io.onrender.com/
```
Expected: `{"message": "Doctor Appointment System API"}`

**B. Get Doctors**
```
https://luciansans-github-io.onrender.com/api/doctors
```
Expected: JSON array of doctors (might be empty `[]`)

**C. Test Registration (using browser console)**
Open browser console (F12) and run:
```javascript
fetch('https://luciansans-github-io.onrender.com/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'testuser123',
    email: 'test@example.com',
    password: 'testpass123',
    role: 'Patient'
  })
})
.then(r => r.json())
.then(d => console.log('Success:', d))
.catch(e => console.error('Error:', e));
```

Expected: `{"message": "User registered successfully", "user_id": 1, "username": "testuser123"}`

### 4. Test the Frontend

**A. Open GitHub Pages Site**
```
https://luciansans.github.io
```

**B. Open Browser Console (F12)**
Check for:
- ✅ No CORS errors
- ✅ `API_BASE_URL` should be `https://luciansans-github-io.onrender.com/api`

**C. Try to Register**
1. Click "Register" in the navigation
2. Fill in the form:
   - Username: `testuser456`
   - Email: `test2@example.com`
   - Password: `password123`
   - Role: Patient
3. Click "Register"

**Expected**: Success message "Registration successful! Please login."

## Common Issues and Solutions

### Issue 1: "Deploy live for 9e3af6d" (Old Commit)
**Problem**: Render is still deploying the old commit
**Solution**: 
1. Go to Render dashboard
2. Click "Manual Deploy" → "Clear build cache & deploy"
3. Wait for deployment to complete

### Issue 2: CORS Errors in Browser Console
**Problem**: `Access-Control-Allow-Origin` error
**Solution**: Check `backend/app/core/config.py` has:
```python
CORS_ORIGINS: list = ["https://luciansans.github.io", "http://localhost:3000"]
```

### Issue 3: "password cannot be longer than 72 bytes"
**Problem**: Password truncation not working
**Solution**: This means `security.py` changes aren't deployed. Check:
1. Is commit `2b2f170` actually deployed? (Check Render dashboard)
2. Does the commit include `security.py` changes? Run: `git show 2b2f170:backend/app/core/security.py`

### Issue 4: "404 Not Found" for `/api/auth/register`
**Problem**: API endpoint not found
**Solution**: Check Render logs for startup errors

### Issue 5: Frontend Shows Old Code
**Problem**: GitHub Pages is caching old files
**Solution**: 
1. Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Clear browser cache
3. Try incognito/private browsing mode

## Verification Checklist

- [ ] Render shows "Deploy live for 2b2f170"
- [ ] Render logs show "Application startup complete"
- [ ] Backend health check returns JSON response
- [ ] `/api/doctors` endpoint works
- [ ] Direct API registration test succeeds
- [ ] Frontend loads without errors
- [ ] Browser console shows correct API_BASE_URL
- [ ] Frontend registration form works

## If Still Not Working

1. **Check Git History**
   ```bash
   cd luciansans.github.io
   git log --oneline -5 --name-only
   ```
   Verify that `security.py` and `auth.py` appear in the history.

2. **Verify File Contents on GitHub**
   - Go to: https://github.com/luciansans/luciansans.github.io
   - Navigate to: `backend/app/core/security.py`
   - Check lines 16-26 for password truncation code

3. **Check Render Environment Variables**
   - Go to Render dashboard → Environment
   - Verify `SECRET_KEY` is set
   - Verify `DATABASE_URL` is set (if using PostgreSQL)

4. **Force Redeploy**
   ```bash
   cd luciansans.github.io
   git commit --allow-empty -m "Force redeploy"
   git push origin main
   ```
   Then manually deploy on Render.

## Contact Information

If you're still experiencing issues after following this guide:
1. Share the exact error message from Render logs
2. Share the browser console error (if any)
3. Confirm which commit is actually deployed on Render