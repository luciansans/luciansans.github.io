from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from ..core.database import get_db
from ..api.auth import get_current_user
from ..models.user import User
from ..models.patient import Patient

router = APIRouter()


@router.get("/")
def list_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all patients."""
    patients = db.query(Patient).offset(skip).limit(limit).all()
    return patients


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_patient(
    full_name: str,
    gender: str,
    date_of_birth: str,
    contact_number: str,
    email: str = None,
    address: str = None,
    medical_history: str = None,
    consent_flag: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new patient."""
    # Check if patient with same contact exists
    existing = db.query(Patient).filter(Patient.contact_number == contact_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Patient with this contact number already exists")
    
    # Parse date
    try:
        dob = date.fromisoformat(date_of_birth)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    new_patient = Patient(
        full_name=full_name,
        gender=gender,
        date_of_birth=dob,
        contact_number=contact_number,
        email=email,
        address=address,
        medical_history=medical_history,
        consent_flag=consent_flag
    )
    
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    
    return new_patient


@router.get("/{patient_id}")
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get patient by ID."""
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{patient_id}")
def update_patient(
    patient_id: int,
    full_name: str = None,
    contact_number: str = None,
    email: str = None,
    address: str = None,
    medical_history: str = None,
    consent_flag: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update patient information."""
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    if full_name:
        patient.full_name = full_name
    if contact_number:
        patient.contact_number = contact_number
    if email:
        patient.email = email
    if address:
        patient.address = address
    if medical_history:
        patient.medical_history = medical_history
    if consent_flag is not None:
        patient.consent_flag = consent_flag
    
    db.commit()
    db.refresh(patient)
    
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete patient."""
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(patient)
    db.commit()
    
    return None