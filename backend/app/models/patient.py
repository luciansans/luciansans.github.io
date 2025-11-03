from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Patient(Base):
    """Patient model representing clinic patients."""
    
    __tablename__ = "patients"
    
    patient_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    contact_number = Column(String(15), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=True, index=True)
    address = Column(Text, nullable=True)
    medical_history = Column(Text, nullable=True)
    consent_flag = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="patient")
    user = relationship("User", foreign_keys="User.patient_id", back_populates="patient", uselist=False)
    
    def __repr__(self):
        return f"<Patient(id={self.patient_id}, name='{self.full_name}')>"