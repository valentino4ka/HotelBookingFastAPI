from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from app.models.booking import Booking, BookingStatus, PaymentStatus
from fastapi import HTTPException
import os
from yookassa import Configuration, Payment
import uuid
from typing import Dict, Optional, List
from app.models.room import Room

# Yookassa config
Configuration.account_id = os.getenv("YOOKASSA_SHOP_ID")
Configuration.secret_key = os.getenv("YOOKASSA_SECRET_KEY")

def get_bookings_by_user(db: Session, user_id: int):
    return db.query(Booking).filter(Booking.user_id == user_id).all()

def get_booking_by_id(db: Session, booking_id: int, user_id: int = None):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if user_id and booking.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your booking")
    return booking

def cancel_booking(db: Session, booking_id: int, user_id: int):
    db_booking = get_booking_by_id(db, booking_id, user_id)
    if db_booking.booking_status not in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
        raise HTTPException(status_code=400, detail="Cannot cancel this booking")
    db_booking.booking_status = BookingStatus.CANCELLED
    db.commit()
    db.refresh(db_booking)
    return db_booking

# Для админа: полный CRUD
def create_booking(db: Session, booking_create: dict):
    db_booking = Booking(**booking_create)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def update_booking(db: Session, booking_id: int, booking_update: dict):
    db_booking = get_booking_by_id(db, booking_id)
    for key, value in booking_update.items():
        if value is not None:
            setattr(db_booking, key, value)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def delete_booking(db: Session, booking_id: int):
    db_booking = get_booking_by_id(db, booking_id)
    db.delete(db_booking)
    db.commit()

# 2. Основная логика создания бронирования с Yookassa
# ----------------------------------------------------------------------
def create_booking(db: Session, data: Dict, user_id: int) -> Booking:
    # ---- проверка комнаты и дат ----
    room = db.query(Room).filter(Room.id == data["room_id"]).first()
    if not room or not room.is_available:
        raise HTTPException(status_code=404, detail="Room not available")

    check_in = data["check_in_date"]
    check_out = data["check_out_date"]
    if check_in >= check_out:
        raise HTTPException(status_code=400, detail="Invalid dates")

    # ---- доступность ----
    booked_count = db.query(func.count(Booking.id)).filter(
        Booking.room_id == room.id,
        Booking.booking_status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED, BookingStatus.CHECKED_IN]),
        or_((Booking.check_in_date < check_out) & (Booking.check_out_date > check_in))
    ).scalar() or 0

    if booked_count >= room.quantity:
        raise HTTPException(status_code=400, detail="No rooms available")

    # ---- расчёт цены ----
    nights = (check_out - check_in).days
    subtotal = room.price_per_night * nights
    cleaning = room.cleaning_fee or 0.0
    service = subtotal * 0.05
    tax = subtotal * 0.13
    total = subtotal + cleaning + service + tax

    booking_code = f"HB{uuid.uuid4().hex[:12].upper()}"
    idempotency_key = str(uuid.uuid4())

    # ---- создаём запись ----
    booking = Booking(
        user_id=user_id,
        room_id=room.id,
        check_in_date=check_in,
        check_out_date=check_out,
        num_guests=data["num_guests"],
        guest_name=data["guest_name"],
        guest_email=data["guest_email"],
        guest_phone=data.get("guest_phone"),
        special_requests=data.get("special_requests"),
        price_per_night=room.price_per_night,
        total_nights=nights,
        subtotal=subtotal,
        cleaning_fee=cleaning,
        service_fee=service,
        tax=tax,
        total_price=total,
        booking_status=BookingStatus.PENDING,
        payment_status=PaymentStatus.PENDING,
        booking_code=booking_code,
        idempotency_key=idempotency_key
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    # ---- платёж Yookassa ----
    try:
        payment = Payment.create({
            "amount": {"value": f"{total:.2f}", "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": "http://localhost:3000/booking-success"  # заменить при наличии фронта
            },
            "capture": True,
            "description": f"Бронирование {booking_code}",
            "metadata": {"booking_id": str(booking.id)},
            "receipt": {"customer": {"email": data["guest_email"]}}
        }, idempotency_key)

        booking.payment_id = payment.id
        booking.confirmation_url = payment.confirmation.confirmation_url
        db.commit()
        db.refresh(booking)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Yookassa error: {str(e)}")

    return booking

# ----------------------------------------------------------------------
# 3. Вспомогательные функции
# ----------------------------------------------------------------------
def update_payment_status(db: Session, booking_id: int, payment_status: PaymentStatus, booking_status: BookingStatus):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        booking.payment_status = payment_status
        booking.booking_status = booking_status
        db.commit()
        db.refresh(booking)
    return booking

def cancel_booking(db: Session, booking_id: int, user_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == user_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.booking_status not in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
        raise HTTPException(status_code=400, detail="Cannot cancel this booking")

    booking.booking_status = BookingStatus.CANCELLED
    booking.payment_status = PaymentStatus.REFUNDED
    db.commit()
    db.refresh(booking)
    return booking