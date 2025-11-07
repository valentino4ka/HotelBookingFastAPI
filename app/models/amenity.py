from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base
from app.models.base import TimestampMixin


# Промежуточная таблица для связи многие-ко-многим: Отель <-> Удобства
hotel_amenities = Table(
    'hotel_amenities',
    Base.metadata,
    Column('hotel_id', Integer, ForeignKey('hotels.id', ondelete='CASCADE'), primary_key=True),
    Column('amenity_id', Integer, ForeignKey('amenities.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=False)
)

# Промежуточная таблица для связи многие-ко-многим: Номер <-> Удобства
room_amenities = Table(
    'room_amenities',
    Base.metadata,
    Column('room_id', Integer, ForeignKey('rooms.id', ondelete='CASCADE'), primary_key=True),
    Column('amenity_id', Integer, ForeignKey('amenities.id', ondelete='CASCADE'), primary_key=True)
)


class Amenity(Base, TimestampMixin):
    """Модель удобств (Wi-Fi, парковка, бассейн и т.д.)"""
    __tablename__ = "amenities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)  # Название иконки для UI
    category = Column(String(50), nullable=True, index=True)  # general, room, bathroom, kitchen и т.д.

    def __repr__(self):
        return f"<Amenity(id={self.id}, name={self.name})>"