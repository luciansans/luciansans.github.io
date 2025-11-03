from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Doctor(Base):
    """Doctor model representing medical practitioners."""
    
    __tablename__ = "doctors"
    
    doctor_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    contact_number = Column(String(15), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    room_number = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="doctor")
    user = relationship("User", foreign_keys="User.doctor_id", back_populates="doctor", uselist=False)
    
    def __repr__(self):
        return f"<Doctor(id={self.doctor_id}, name='{self.full_name}', specialty='{self.specialization}')>"