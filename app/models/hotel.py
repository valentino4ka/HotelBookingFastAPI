from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import TimestampMixin, SoftDeleteMixin
from app.models.amenity import hotel_amenities


class Hotel(Base, TimestampMixin, SoftDeleteMixin):
    """Модель отеля"""
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    
    # Основная информация
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Адрес и локация
    country = Column(String(100), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)
    address = Column(String(500), nullable=False)
    postal_code = Column(String(20), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Контактная информация
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)
    
    # Изображения (JSON массив URL)
    images = Column(JSON, nullable=True, default=list)
    main_image = Column(String(500), nullable=True)
    
    # Рейтинг и статистика
    rating = Column(Float, default=0.0, nullable=False)
    total_reviews = Column(Integer, default=0, nullable=False)
    
    # Статус
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Правила отеля
    check_in_time = Column(String(10), default="14:00", nullable=False)
    check_out_time = Column(String(10), default="12:00", nullable=False)
    cancellation_policy = Column(Text, nullable=True)
    house_rules = Column(Text, nullable=True)
    
    # Связь с менеджером
    manager_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Связи
    manager = relationship(
        "User",
        back_populates="managed_hotels",
        lazy="select"
    )
    
    rooms = relationship(
        "Room",
        back_populates="hotel",
        lazy="select",
        cascade="all, delete-orphan"
    )
    
    reviews = relationship(
        "Review",
        back_populates="hotel",
        lazy="select",
        cascade="all, delete-orphan"
    )
    
    amenities = relationship(
        "Amenity",
        secondary=hotel_amenities,
        lazy="select"
    )

    def __repr__(self):
        return f"<Hotel(id={self.id}, name={self.name}, city={self.city})>"