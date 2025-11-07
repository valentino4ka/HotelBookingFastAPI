from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.database import Base
from app.models.base import TimestampMixin, SoftDeleteMixin
from app.models.amenity import room_amenities


class RoomType(str, enum.Enum):
    """Типы номеров"""
    SINGLE = "single"
    DOUBLE = "double"
    TWIN = "twin"
    SUITE = "suite"
    DELUXE = "deluxe"
    APARTMENT = "apartment"
    STUDIO = "studio"


class BedType(str, enum.Enum):
    """Типы кроватей"""
    SINGLE = "single"
    DOUBLE = "double"
    QUEEN = "queen"
    KING = "king"
    SOFA_BED = "sofa_bed"


class Room(Base, TimestampMixin, SoftDeleteMixin):
    """Модель номера"""
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    
    # Связь с отелем
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Основная информация
    name = Column(String(255), nullable=False)
    room_number = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    room_type = Column(SQLEnum(RoomType), nullable=False, index=True)
    
    # Характеристики
    size_sqm = Column(Float, nullable=True)  # Площадь в квадратных метрах
    max_guests = Column(Integer, nullable=False, default=2)
    num_beds = Column(Integer, nullable=False, default=1)
    bed_type = Column(SQLEnum(BedType), nullable=False, default=BedType.DOUBLE)
    
    # Количество комнат
    num_bedrooms = Column(Integer, default=1, nullable=False)
    num_bathrooms = Column(Integer, default=1, nullable=False)
    
    # Цены
    price_per_night = Column(Float, nullable=False)
    weekend_price = Column(Float, nullable=True)  # Цена на выходные (опционально)
    cleaning_fee = Column(Float, default=0.0, nullable=False)
    
    # Изображения
    images = Column(JSON, nullable=True, default=list)
    main_image = Column(String(500), nullable=True)
    
    # Доступность
    is_available = Column(Boolean, default=True, nullable=False, index=True)
    quantity = Column(Integer, default=1, nullable=False)  # Количество таких номеров
    
    # Связи
    hotel = relationship(
        "Hotel",
        back_populates="rooms",
        lazy="select"
    )
    
    bookings = relationship(
        "Booking",
        back_populates="room",
        lazy="select",
        cascade="all, delete-orphan"
    )
    
    amenities = relationship(
        "Amenity",
        secondary=room_amenities,
        lazy="select"
    )

    def __repr__(self):
        return f"<Room(id={self.id}, hotel_id={self.hotel_id}, name={self.name})>"