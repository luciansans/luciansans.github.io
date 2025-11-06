# PostgreSQL Setup Guide for Render

## Why PostgreSQL?

Your SQLite database is stored in Render's ephemeral filesystem, which means:
- ❌ Data is lost when the service restarts
- ❌ Data is lost when you redeploy
- ❌ Doctors, appointments, and users disappear

PostgreSQL provides:
- ✅ Persistent data storage
- ✅ Better performance
- ✅ Production-ready database
- ✅ Free tier available on Render

## Step-by-Step Setup

### Step 1: Create PostgreSQL Database on Render

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com

2. **Create New PostgreSQL Database**
   - Click "New +" button (top right)
   - Select "PostgreSQL"

3. **Configure Database**
   - **Name**: `clinic-database` (or any name you prefer)
   - **Database**: `clinic_db` (will be created automatically)
   - **User**: `clinic_user` (will be created automatically)
   - **Region**: Choose same as your web service (Oregon)
   - **PostgreSQL Version**: 16 (latest)
   - **Plan**: **Free** (perfect for development/testing)

4. **Create Database**
   - Click "Create Database"
   - Wait 2-3 minutes for provisioning

5. **Note the Connection Details**
   After creation, you'll see:
   - **Internal Database URL** (use this one!)
   - **External Database URL**
   - Hostname, Port, Database name, Username, Password

### Step 2: Connect Database to Your Web Service

1. **Go to Your Web Service**
   - In Render dashboard, click on your service "clinic-backend"

2. **Go to Environment Tab**
   - Click "Environment" in the left sidebar

3. **Update DATABASE_URL**
   - Find the `DATABASE_URL` environment variable
   - Click "Edit" or "Add Environment Variable" if it doesn't exist
   - **Key**: `DATABASE_URL`
   - **Value**: Click "Connect to Database"
   - Select your PostgreSQL database: `clinic-database`
   - Render will automatically fill in the Internal Database URL

4. **Save Changes**
   - Click "Save Changes"
   - This will trigger a redeploy automatically

### Step 3: Update requirements.txt

Add PostgreSQL driver to your dependencies:

```txt
# Add this line to backend/requirements.txt
psycopg2-binary==2.9.9
```

I'll do this for you now...

### Step 4: Verify Database Connection

After the redeploy completes:

1. **Check Render Logs**
   Look for:
   ```
   ✅ Successfully installed psycopg2-binary-2.9.9
   ✅ INFO: Application startup complete
   ```

2. **Test Database Connection**
   The application will automatically:
   - Connect to PostgreSQL using the DATABASE_URL
   - Create all necessary tables on first run
   - Store all data persistently

### Step 5: Test Your Application

1. **Register a New User**
   - Go to https://luciansans.github.io
   - Register as a Doctor
   - Username: `dr_smith`
   - Email: `doctor@example.com`
   - Password: `password123`
   - Role: **Doctor**

2. **Add Doctor Profile**
   You'll need to add doctor details through the API or admin interface

3. **Verify Persistence**
   - Restart your Render service (Manual Deploy)
   - Check that doctors still appear
   - Data should persist!

## Database Schema

Your application will automatically create these tables:

1. **users** - All user accounts (patients, doctors, reception)
2. **doctors** - Doctor profiles (specialization, contact info)
3. **patients** - Patient profiles (medical history)
4. **appointments** - Appointment bookings
5. **queue** - Queue management
6. **notifications** - System notifications

## Troubleshooting

### Issue: "Could not connect to database"

**Solution:**
1. Check that DATABASE_URL is set correctly in Render environment
2. Verify PostgreSQL database is running (green status in Render)
3. Make sure you're using the **Internal Database URL**, not External

### Issue: "relation does not exist"

**Solution:**
The tables haven't been created yet. The application should create them automatically on startup. If not, you may need to run migrations.

### Issue: "too many connections"

**Solution:**
Free tier PostgreSQL has a connection limit. Make sure your application:
- Closes database connections properly (it should with SQLAlchemy)
- Doesn't create too many concurrent connections

## Cost

- **PostgreSQL Free Tier**: 
  - ✅ 256 MB RAM
  - ✅ 1 GB Storage
  - ✅ Perfect for development and small applications
  - ✅ $0/month

- **Upgrade Options** (if needed later):
  - Starter: $7/month (1 GB RAM, 10 GB storage)
  - Standard: $20/month (4 GB RAM, 50 GB storage)

## Next Steps After Setup

1. **Seed Initial Data**
   - Create some doctor accounts
   - Add doctor profiles
   - Test appointment booking

2. **Backup Strategy** (for production)
   - Render provides automatic daily backups
   - You can also export data manually

3. **Monitor Usage**
   - Check database size in Render dashboard
   - Monitor connection count
   - Review query performance

## Migration from SQLite to PostgreSQL

Your application code doesn't need changes! SQLAlchemy handles both databases:

```python
# This works for both SQLite and PostgreSQL
DATABASE_URL: str = "sqlite:///./clinic.db"  # Local development
DATABASE_URL: str = "postgresql://..."        # Production (from env var)
```

The `DATABASE_URL` environment variable on Render will override the default SQLite URL.

## Summary

1. ✅ Create PostgreSQL database on Render
2. ✅ Connect it to your web service via DATABASE_URL
3. ✅ Add psycopg2-binary to requirements.txt
4. ✅ Redeploy
5. ✅ Test - data will now persist!

Your doctors, appointments, and users will no longer disappear! 🎉