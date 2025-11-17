# app/models/location_category.py
from sqlalchemy import Column, Integer, String, Text
from app.database import Base
from app.models.base import TimestampMixin


class LocationCategory(Base, TimestampMixin):
    __tablename__ = "location_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<LocationCategory(id={self.id}, name={self.name})>"