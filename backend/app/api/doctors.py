from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..api.auth import get_current_user
from ..models.user import User
from ..models.doctor import Doctor

router = APIRouter()


@router.get("/")
def list_doctors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all doctors (public endpoint)."""
    doctors = db.query(Doctor).offset(skip).limit(limit).all()
    return doctors


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_doctor(
    full_name: str,
    specialization: str,
    contact_number: str,
    email: str,
    room_number: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new doctor (admin only)."""
    # Check if doctor with same email exists
    existing = db.query(Doctor).filter(Doctor.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Doctor with this email already exists")
    
    new_doctor = Doctor(
        full_name=full_name,
        specialization=specialization,
        contact_number=contact_number,
        email=email,
        room_number=room_number
    )
    
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    
    return new_doctor


@router.get("/{doctor_id}")
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    """Get doctor by ID."""
    doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.put("/{doctor_id}")
def update_doctor(
    doctor_id: int,
    full_name: str = None,
    specialization: str = None,
    contact_number: str = None,
    email: str = None,
    room_number: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update doctor information."""
    doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    if full_name:
        doctor.full_name = full_name
    if specialization:
        doctor.specialization = specialization
    if contact_number:
        doctor.contact_number = contact_number
    if email:
        doctor.email = email
    if room_number:
        doctor.room_number = room_number
    
    db.commit()
    db.refresh(doctor)
    
    return doctor


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete doctor."""
    doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db.delete(doctor)
    db.commit()
    
    return None