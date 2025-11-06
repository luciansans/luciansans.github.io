# Doctor Appointment System - Backend

FastAPI backend for the Doctor Appointment and Office Management System.

## Quick Start

### Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the Server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API**:
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/health

## Deployment to Render

See [DEPLOYMENT.md](../DEPLOYMENT.md) for complete deployment instructions.

### Quick Deploy Steps:

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect your repository
4. Set root directory to `backend`
5. Configure environment variables
6. Deploy!

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Patients
- `GET /api/patients/` - List all patients
- `POST /api/patients/` - Create patient
- `GET /api/patients/{id}` - Get patient details
- `PUT /api/patients/{id}` - Update patient
- `DELETE /api/patients/{id}` - Delete patient

### Doctors
- `GET /api/doctors/` - List all doctors
- `POST /api/doctors/` - Create doctor
- `GET /api/doctors/{id}` - Get doctor details
- `PUT /api/doctors/{id}` - Update doctor
- `DELETE /api/doctors/{id}` - Delete doctor

### Appointments
- `GET /api/appointments/` - List appointments
- `POST /api/appointments/` - Create appointment
- `GET /api/appointments/{id}` - Get appointment details
- `PUT /api/appointments/{id}` - Update appointment
- `DELETE /api/appointments/{id}` - Cancel appointment

### Queue Management
- `GET /api/queue/status/{doctor_id}` - Get queue status
- `POST /api/queue/check-in` - Check in patient
- `POST /api/queue/call-next/{doctor_id}` - Call next patient

## Environment Variables

Required environment variables (see `.env.example`):

- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT secret key (use strong random value)
- `CORS_ORIGINS` - Allowed origins for CORS
- `DEBUG` - Debug mode (False for production)

## Database

### SQLite (Development)
Default configuration uses SQLite for easy local development.

### PostgreSQL (Production)
For production on Render, use PostgreSQL:

1. Create PostgreSQL database on Render
2. Update `DATABASE_URL` environment variable
3. Add `psycopg2-binary` to requirements.txt

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── api/                 # API endpoints
│   │   ├── auth.py
│   │   ├── appointments.py
│   │   ├── doctors.py
│   │   ├── patients.py
│   │   └── queue.py
│   ├── core/                # Core functionality
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database setup
│   │   └── security.py      # Security utilities
│   └── models/              # Database models
│       ├── user.py
│       ├── patient.py
│       ├── doctor.py
│       ├── appointment.py
│       ├── queue.py
│       └── notification.py
├── requirements.txt         # Python dependencies
├── render.yaml             # Render deployment config
└── .env.example            # Environment variables template
```

## Testing

Run tests with pytest:
```bash
pytest
```

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- SQL injection prevention (SQLAlchemy ORM)
- Input validation with Pydantic

## Support

For deployment issues, see [DEPLOYMENT.md](../DEPLOYMENT.md)