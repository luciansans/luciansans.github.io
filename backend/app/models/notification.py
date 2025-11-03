from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base


class NotificationChannel(str, enum.Enum):
    """Enumeration for notification channels."""
    SMS = "sms"
    EMAIL = "email"
    WHATSAPP = "whatsapp"


class NotificationStatus(str, enum.Enum):
    """Enumeration for notification delivery status."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"


class Notification(Base):
    """Notification model for tracking messages sent to patients."""
    
    __tablename__ = "notifications"
    
    notification_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.appointment_id"), nullable=False)
    channel = Column(Enum(NotificationChannel), nullable=False)
    template_name = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    recipient = Column(String(100), nullable=False)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING)
    sent_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    appointment = relationship("Appointment", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification(id={self.notification_id}, channel='{self.channel}', status='{self.status}')>"