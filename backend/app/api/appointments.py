from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from ..core.database import get_db
from ..api.auth import get_current_user
from ..models.user import User
from ..models.appointment import Appointment, AppointmentStatus, AppointmentType
from ..models.doctor import Doctor

router = APIRouter()


def check_slot_availability(
    db: Session,
    doctor_id: int,
    start_time: datetime,
    end_time: datetime,
    exclude_appointment_id: int = None
) -> bool:
    """Check if a time slot is available for a doctor."""
    query = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.status.in_([
            AppointmentStatus.SCHEDULED,
            AppointmentStatus.CHECKED_IN,
            AppointmentStatus.IN_PROGRESS
        ]),
        Appointment.appointment_date < end_time,
        Appointment.end_time > start_time
    )
    
    if exclude_appointment_id:
        query = query.filter(Appointment.appointment_id != exclude_appointment_id)
    
    return query.count() == 0


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_appointment(
    patient_id: int,
    doctor_id: int,
    appointment_date: str,  # ISO format: YYYY-MM-DDTHH:MM:SS
    appointment_type: str,
    reason: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new appointment."""
    # Parse datetime
    try:
        start_time = datetime.fromisoformat(appointment_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format")
    
    # Calculate end time (30 minutes)
    end_time = start_time + timedelta(minutes=30)
    
    # Check slot availability
    if not check_slot_availability(db, doctor_id, start_time, end_time):
        raise HTTPException(status_code=400, detail="Selected time slot is not available")
    
    # Verify doctor exists
    doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Create appointment
    new_appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        appointment_date=start_time,
        end_time=end_time,
        appointment_type=AppointmentType(appointment_type),
        reason=reason,
        created_by=current_user.user_id
    )
    
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    
    return new_appointment


@router.get("/")
def list_appointments(
    skip: int = 0,
    limit: int = 100,
    patient_id: int = None,
    doctor_id: int = None,
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List appointments with optional filters."""
    query = db.query(Appointment)
    
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)
    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    if status_filter:
        query = query.filter(Appointment.status == AppointmentStatus(status_filter))
    
    appointments = query.offset(skip).limit(limit).all()
    return appointments


@router.get("/{appointment_id}")
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get appointment by ID."""
    appointment = db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    return appointment


@router.put("/{appointment_id}")
def update_appointment(
    appointment_id: int,
    appointment_date: str = None,
    status_update: str = None,
    reason: str = None,
    notes: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing appointment."""
    appointment = db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # If rescheduling
    if appointment_date:
        try:
            new_start = datetime.fromisoformat(appointment_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid datetime format")
        
        new_end = new_start + timedelta(minutes=30)
        
        if not check_slot_availability(db, appointment.doctor_id, new_start, new_end, appointment_id):
            raise HTTPException(status_code=400, detail="New time slot is not available")
        
        appointment.appointment_date = new_start
        appointment.end_time = new_end
    
    if status_update:
        appointment.status = AppointmentStatus(status_update)
    if reason:
        appointment.reason = reason
    if notes:
        appointment.notes = notes
    
    db.commit()
    db.refresh(appointment)
    
    return appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel an appointment."""
    appointment = db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment.status = AppointmentStatus.CANCELLED
    db.commit()
    
    return None


@router.get("/doctor/{doctor_id}/schedule")
def get_doctor_schedule(
    doctor_id: int,
    date: str,  # Format: YYYY-MM-DD
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get doctor's schedule for a specific date."""
    try:
        schedule_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    start_of_day = schedule_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    
    appointments = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date >= start_of_day,
        Appointment.appointment_date < end_of_day,
        Appointment.status != AppointmentStatus.CANCELLED
    ).order_by(Appointment.appointment_date).all()
    
    return appointments