# Quick Start: PostgreSQL Setup

## 🚀 5-Minute Setup

### 1. Create PostgreSQL Database (2 minutes)

1. Go to https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Fill in:
   - **Name**: `clinic-database`
   - **Region**: Oregon (same as your web service)
   - **Plan**: **Free**
4. Click "Create Database"
5. Wait for green "Available" status

### 2. Connect to Your Web Service (1 minute)

1. Go to your web service "clinic-backend"
2. Click "Environment" tab
3. Find or add `DATABASE_URL` variable
4. Click "Connect to Database"
5. Select `clinic-database`
6. Click "Save Changes"

### 3. Deploy (2 minutes)

Render will automatically redeploy with the new database connection.

**OR** manually trigger:
1. Click "Manual Deploy"
2. Select latest commit: `d3c2901`
3. Wait for deployment

### 4. Verify (30 seconds)

Check Render logs for:
```
✅ Successfully installed psycopg2-binary-2.9.9
✅ INFO: Application startup complete
```

### 5. Test (1 minute)

1. Go to https://luciansans.github.io
2. Register as a Doctor
3. Create doctor profile
4. Restart Render service
5. Check that doctor still appears ✅

## That's It!

Your data will now persist across restarts and redeployments! 🎉

## What Changed?

- ✅ Added `psycopg2-binary==2.9.9` to requirements.txt
- ✅ Committed and pushed to GitHub
- ✅ Ready to connect PostgreSQL database

## Need Help?

See detailed guide: `POSTGRESQL_SETUP.md`

## Current Status

- **Commit**: `d3c2901` - "Add PostgreSQL support with psycopg2-binary"
- **Status**: Ready to deploy with PostgreSQL
- **Action Required**: Create PostgreSQL database on Render and connect it

## Benefits

Before (SQLite):
- ❌ Data lost on restart
- ❌ Doctors disappear
- ❌ Appointments lost

After (PostgreSQL):
- ✅ Persistent data
- ✅ Doctors remain
- ✅ Appointments saved
- ✅ Production-ready