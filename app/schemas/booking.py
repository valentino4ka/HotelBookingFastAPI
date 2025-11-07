from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.booking import BookingStatus, PaymentStatus

class BookingOut(BaseModel):
    id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    num_guests: int
    total_price: float
    booking_status: BookingStatus
    payment_status: PaymentStatus
    created_at: datetime

    class Config:
        from_attributes = True