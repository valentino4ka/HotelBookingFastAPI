from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.booking import BookingCreate, BookingOut
from app.crud.booking import create_booking, get_bookings_by_user, get_booking_by_id, cancel_booking, update_payment_status
from app.routers.auth import get_current_user_from_cookie
from app.models.user import User
from app.models.booking import PaymentStatus, BookingStatus
from yookassa.domain.notification import WebhookNotification

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/create", response_model=BookingOut)
def create_booking_endpoint(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_cookie)
):
    return create_booking(db, booking.dict(), current_user.id)

@router.get("/", response_model=List[BookingOut])
def list_my_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    return get_bookings_by_user(db, current_user.id)

@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    return get_booking_by_id(db, booking_id, current_user.id)

@router.delete("/{booking_id}")
def cancel_booking_endpoint(booking_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    cancel_booking(db, booking_id, current_user.id)
    return {"message": "Booking cancelled"}

@router.post("/webhook")
async def yookassa_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    try:
        notification = WebhookNotification(payload)
        payment = notification.object
        booking_id = int(payment.metadata.get("booking_id", 0)) if payment.metadata else 0

        if payment.status == "succeeded":
            update_payment_status(db, booking_id, PaymentStatus.PAID, BookingStatus.CONFIRMED)
        elif payment.status == "canceled":
            update_payment_status(db, booking_id, PaymentStatus.FAILED, BookingStatus.REJECTED)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

    return {"status": "ok"}