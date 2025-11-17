# app/models/event.py
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import TimestampMixin


class Event(Base, TimestampMixin):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    event_date_start = Column(DateTime(timezone=True), nullable=False, index=True)
    event_date_end = Column(DateTime(timezone=True), nullable=True)
    
    location = Column(String(500), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    city = Column(String(100), nullable=False, index=True)
    country = Column(String(100), nullable=False)
    
    ticket_url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    is_free = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Event(id={self.id}, title={self.title})>"