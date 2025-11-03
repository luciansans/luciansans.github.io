from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base


class AppointmentStatus(str, enum.Enum):
    """Enumeration for appointment status."""
    SCHEDULED = "scheduled"
    CHECKED_IN = "checked_in"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class AppointmentType(str, enum.Enum):
    """Enumeration for appointment types."""
    CONSULTATION = "consultation"
    FOLLOW_UP = "follow_up"
    EMERGENCY = "emergency"
    ROUTINE_CHECKUP = "routine_checkup"


class Appointment(Base):
    """Appointment model representing patient-doctor appointments."""
    
    __tablename__ = "appointments"
    
    appointment_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"), nullable=False)
    appointment_date = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    appointment_type = Column(Enum(AppointmentType), nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED)
    reason = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    creator = relationship("User", foreign_keys=[created_by])
    notifications = relationship("Notification", back_populates="appointment")
    queue_entry = relationship("QueueEntry", back_populates="appointment", uselist=False)
    
    # Composite index for efficient queries
    __table_args__ = (
        Index('idx_doctor_date', 'doctor_id', 'appointment_date'),
    )
    
    def __repr__(self):
        return f"<Appointment(id={self.appointment_id}, patient={self.patient_id}, doctor={self.doctor_id}, date='{self.appointment_date}')>"