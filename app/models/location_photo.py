# app/models/location_photo.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import TimestampMixin


class LocationPhoto(Base, TimestampMixin):
    __tablename__ = "location_photos"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False, index=True)
    url = Column(String(500), nullable=False)
    caption = Column(String(255), nullable=True)
    is_main = Column(Integer, default=0, nullable=False)  # 1 = главная

    location = relationship("Location", back_populates="photos")

    def __repr__(self):
        return f"<LocationPhoto(id={self.id}, location_id={self.location_id})>"