from sqlalchemy.orm import Session
from app.models.booking import Booking, BookingStatus
from fastapi import HTTPException

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