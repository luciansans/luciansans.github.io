from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base


class QueuePriority(str, enum.Enum):
    """Enumeration for queue priority levels."""
    ROUTINE = "routine"
    URGENT = "urgent"
    EMERGENCY = "emergency"


class QueueStatus(str, enum.Enum):
    """Enumeration for queue entry status."""
    WAITING = "waiting"
    CALLED = "called"
    IN_CONSULTATION = "in_consultation"
    SKIPPED = "skipped"
    COMPLETED = "completed"


class QueueEntry(Base):
    """Queue entry model for managing patient flow."""
    
    __tablename__ = "queue_entries"
    
    queue_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.appointment_id"), unique=True, nullable=False)
    check_in_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    priority = Column(Enum(QueuePriority), default=QueuePriority.ROUTINE)
    position = Column(Integer, nullable=True)
    status = Column(Enum(QueueStatus), default=QueueStatus.WAITING)
    called_time = Column(DateTime, nullable=True)
    completed_time = Column(DateTime, nullable=True)
    estimated_wait_minutes = Column(Integer, nullable=True)
    
    # Relationships
    appointment = relationship("Appointment", back_populates="queue_entry")
    
    def __repr__(self):
        return f"<QueueEntry(id={self.queue_id}, appointment={self.appointment_id}, status='{self.status}')>"