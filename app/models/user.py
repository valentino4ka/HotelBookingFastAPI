from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
import enum
from app.database import Base
from app.models.base import TimestampMixin, SoftDeleteMixin


class UserRole(str, enum.Enum):
    """Роли пользователей в системе"""
    GUEST = "guest"  # Незарегистрированный (для сессий)
    USER = "user"  # Зарегистрированный пользователь
    HOTEL_MANAGER = "hotel_manager"  # Менеджер отеля
    CONTENT_MODERATOR = "content_moderator"  # Модератор контента
    ADMIN = "admin"  # Администратор


class User(Base, TimestampMixin, SoftDeleteMixin):
    """Модель пользователя"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Персональная информация
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Роль и статус
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Дополнительная информация
    bio = Column(Text, nullable=True)
    language = Column(String(10), default="en", nullable=False)
    
    # Связи (используем lazy='select' для избежания проблем с загрузкой)
    managed_hotels = relationship(
        "Hotel",
        back_populates="manager",
        lazy="select",
        cascade="all, delete-orphan"
    )
    
    bookings = relationship(
        "Booking",
        back_populates="user",
        lazy="select",
        foreign_keys="Booking.user_id"
    )
    
    reviews = relationship(
        "Review",
        back_populates="user",
        lazy="select",
        foreign_keys="Review.user_id"
    )
    
    moderated_reviews = relationship(
        "Review",
        back_populates="moderator",
        lazy="select",
        foreign_keys="Review.moderated_by"
    )
    
    audit_logs = relationship(
        "AuditLog",
        back_populates="user",
        lazy="select"
    )
    
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan", lazy="select")

    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan", lazy="select")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"