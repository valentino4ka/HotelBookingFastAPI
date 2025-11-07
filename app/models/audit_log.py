from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
import enum
from app.database import Base
from app.models.base import TimestampMixin



class ActionType(str, enum.Enum):
    """Типы действий для аудита"""
    # Пользователи
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_REGISTER = "user_register"
    USER_UPDATE = "user_update"
    USER_DELETE = "user_delete"
    
    # Отели
    HOTEL_CREATE = "hotel_create"
    HOTEL_UPDATE = "hotel_update"
    HOTEL_DELETE = "hotel_delete"
    
    # Номера
    ROOM_CREATE = "room_create"
    ROOM_UPDATE = "room_update"
    ROOM_DELETE = "room_delete"
    
    # Бронирования
    BOOKING_CREATE = "booking_create"
    BOOKING_UPDATE = "booking_update"
    BOOKING_CANCEL = "booking_cancel"
    
    # Отзывы
    REVIEW_CREATE = "review_create"
    REVIEW_APPROVE = "review_approve"
    REVIEW_REJECT = "review_reject"
    REVIEW_DELETE = "review_delete"
    
    # Система
    SYSTEM_ERROR = "system_error"
    PERMISSION_DENIED = "permission_denied"


class AuditLog(Base, TimestampMixin):
    """Модель логов для аудита действий"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Пользователь, совершивший действие
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Тип действия
    action_type = Column(SQLEnum(ActionType), nullable=False, index=True)
    
    # Описание действия
    description = Column(Text, nullable=True)
    
    # Затронутая сущность
    entity_type = Column(String(50), nullable=True, index=True)  # hotel, room, booking, review и т.д.
    entity_id = Column(Integer, nullable=True, index=True)
    
    # IP адрес и user agent
    ip_address = Column(String(45), nullable=True)  # IPv6 может быть длинным
    user_agent = Column(String(500), nullable=True)
    
    # Дополнительные данные в JSON
    extra_data = Column(JSON, nullable=True)
    
    # Результат действия
    success = Column(Boolean, default=True, nullable=False)
    error_message = Column(Text, nullable=True)
    
    # Связи
    user = relationship(
        "User",
        back_populates="audit_logs",
        lazy="select"
    )

    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action_type}, user_id={self.user_id})>"