from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from ..core.database import get_db
from ..api.auth import get_current_user
from ..models.user import User
from ..models.queue import QueueEntry, QueueStatus, QueuePriority
from ..models.appointment import Appointment

router = APIRouter()


def update_queue_positions(db: Session, doctor_id: int):
    """Update queue positions for a specific doctor."""
    queue_entries = db.query(QueueEntry).join(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        QueueEntry.status == QueueStatus.WAITING
    ).order_by(
        QueueEntry.priority.desc(),
        QueueEntry.check_in_time
    ).all()
    
    for index, entry in enumerate(queue_entries, start=1):
        entry.position = index
        entry.estimated_wait_minutes = (index - 1) * 15  # 15 min average
    
    db.commit()


@router.post("/check-in", status_code=status.HTTP_201_CREATED)
def check_in_patient(
    appointment_id: int,
    priority: str = "routine",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check in a patient and add them to the queue."""
    # Verify appointment exists
    appointment = db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Check if already checked in
    existing_entry = db.query(QueueEntry).filter(
        QueueEntry.appointment_id == appointment_id
    ).first()
    
    if existing_entry:
        raise HTTPException(status_code=400, detail="Patient already checked in")
    
    # Create queue entry
    queue_entry = QueueEntry(
        appointment_id=appointment_id,
        priority=QueuePriority(priority),
        check_in_time=datetime.utcnow()
    )
    
    db.add(queue_entry)
    db.commit()
    
    # Update queue positions
    update_queue_positions(db, appointment.doctor_id)
    
    db.refresh(queue_entry)
    return queue_entry


@router.get("/status/{doctor_id}")
def get_queue_status(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    """Get current queue status for a doctor."""
    queue = db.query(QueueEntry).join(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        QueueEntry.status.in_([QueueStatus.WAITING, QueueStatus.CALLED])
    ).order_by(QueueEntry.position).all()
    
    return queue


@router.post("/call-next/{doctor_id}")
def call_next_patient(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Call the next patient in the queue."""
    next_entry = db.query(QueueEntry).join(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        QueueEntry.status == QueueStatus.WAITING
    ).order_by(
        QueueEntry.priority.desc(),
        QueueEntry.check_in_time
    ).first()
    
    if not next_entry:
        raise HTTPException(status_code=404, detail="No patients in queue")
    
    next_entry.status = QueueStatus.CALLED
    next_entry.called_time = datetime.utcnow()
    
    db.commit()
    
    # Update remaining queue positions
    update_queue_positions(db, doctor_id)
    
    db.refresh(next_entry)
    return next_entry


@router.put("/{queue_id}/complete")
def complete_queue_entry(
    queue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark queue entry as completed."""
    queue_entry = db.query(QueueEntry).filter(QueueEntry.queue_id == queue_id).first()
    
    if not queue_entry:
        raise HTTPException(status_code=404, detail="Queue entry not found")
    
    queue_entry.status = QueueStatus.COMPLETED
    queue_entry.completed_time = datetime.utcnow()
    
    db.commit()
    db.refresh(queue_entry)
    
    return queue_entry


@router.get("/patient/{appointment_id}")
def get_patient_queue_position(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """Get patient's current queue position."""
    queue_entry = db.query(QueueEntry).filter(
        QueueEntry.appointment_id == appointment_id
    ).first()
    
    if not queue_entry:
        raise HTTPException(status_code=404, detail="Patient not in queue")
    
    return {
        "queue_id": queue_entry.queue_id,
        "position": queue_entry.position,
        "status": queue_entry.status.value,
        "estimated_wait_minutes": queue_entry.estimated_wait_minutes,
        "check_in_time": queue_entry.check_in_time.isoformat()
    }