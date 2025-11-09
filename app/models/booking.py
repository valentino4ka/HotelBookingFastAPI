from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
import enum
from app.database import Base
from app.models.base import TimestampMixin


class BookingStatus(str, enum.Enum):
    """Статусы бронирования"""
    PENDING = "pending"  # Ожидает подтверждения
    CONFIRMED = "confirmed"  # Подтверждено
    CHECKED_IN = "checked_in"  # Гость заселился
    CHECKED_OUT = "checked_out"  # Гость выселился
    CANCELLED = "cancelled"  # Отменено
    REJECTED = "rejected"  # Отклонено


class PaymentStatus(str, enum.Enum):
    """Статусы оплаты"""
    PENDING = "pending"
    PAID = "paid"
    REFUNDED = "refunded"
    FAILED = "failed"


class Booking(Base, TimestampMixin):
    """Модель бронирования"""
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    
    # Связи
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Даты
    check_in_date = Column(Date, nullable=False, index=True)
    check_out_date = Column(Date, nullable=False, index=True)
    
    # Гости
    num_guests = Column(Integer, nullable=False, default=1)
    guest_name = Column(String(255), nullable=False)
    guest_email = Column(String(255), nullable=False)
    guest_phone = Column(String(20), nullable=True)
    
    # Цены
    price_per_night = Column(Float, nullable=False)
    total_nights = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)
    cleaning_fee = Column(Float, default=0.0, nullable=False)
    service_fee = Column(Float, default=0.0, nullable=False)
    tax = Column(Float, default=0.0, nullable=False)
    total_price = Column(Float, nullable=False)
    
    # Статусы
    booking_status = Column(
        SQLEnum(BookingStatus),
        default=BookingStatus.PENDING,
        nullable=False,
        index=True
    )
    payment_status = Column(
        SQLEnum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False,
        index=True
    )
    
    payment_id = Column(String(255), nullable=True, index=True)
    idempotency_key = Column(String(255), nullable=True, unique=True)
    confirmation_url = Column(String(500), nullable=True)

    # Дополнительная информация
    special_requests = Column(Text, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    
    # Уникальный код бронирования
    booking_code = Column(String(20), unique=True, nullable=False, index=True)
    
    # Связи
    user = relationship(
        "User",
        back_populates="bookings",
        lazy="select"
    )
    
    room = relationship(
        "Room",
        back_populates="bookings",
        lazy="select"
    )

    def __repr__(self):
        return f"<Booking(id={self.id}, code={self.booking_code}, status={self.booking_status})>"