# app/models/notification.py
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)  # booking_confirmed, review_approved, price_drop и т.д.
    is_read = Column(Boolean, default=False, nullable=False)
    
    related_entity_type = Column(String(50), nullable=True)  # booking, hotel и т.д.
    related_entity_id = Column(Integer, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="notifications", lazy="select")

    def __repr__(self):
        return f"<Notification(id={self.id}, user={self.user_id}, type={self.type})>"