from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.booking import BookingOut
from app.crud.booking import get_bookings_by_user, cancel_booking
from app.routers.auth import get_current_user_from_cookie
from app.models.user import User

router = APIRouter(tags=["user"])

@router.get("/bookings", response_model=List[BookingOut])
def list_my_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    return get_bookings_by_user(db, current_user.id)

@router.delete("/bookings/{booking_id}")
def cancel_my_booking(booking_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    cancel_booking(db, booking_id, current_user.id)
    return {"message": "Booking cancelled"}