# app/models/location.py
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import TimestampMixin, SoftDeleteMixin


class Location(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Адрес
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=False, index=True)
    country = Column(String(100), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Категория
    category_id = Column(Integer, ForeignKey("location_categories.id", ondelete="SET NULL"), nullable=True)
    
    # Дополнительно
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    website = Column(String(500), nullable=True)
    phone = Column(String(30), nullable=True)
    opening_hours = Column(JSON, nullable=True)  # { "monday": "09:00-18:00", ... }
    price_level = Column(Integer, nullable=True)  # 1-4 (дешево → очень дорого)
    is_popular = Column(Boolean, default=False)

    # Связи
    category = relationship("LocationCategory", lazy="select")
    photos = relationship("LocationPhoto", back_populates="location", cascade="all, delete-orphan", lazy="select")
    nearby_hotels = relationship("Hotel", secondary="hotel_nearby_locations", back_populates="nearby_locations", lazy="select")

    def __repr__(self):
        return f"<Location(id={self.id}, name={self.name}, city={self.city})>"