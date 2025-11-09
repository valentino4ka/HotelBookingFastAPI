from pydantic import BaseModel, EmailStr, validator
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

    confirmation_url: Optional[str] = None
    payment_id: Optional[str] = None
    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    room_id: int
    check_in_date: date
    check_out_date: date
    num_guests: int
    guest_name: str
    guest_email: EmailStr
    guest_phone: Optional[str] = None
    special_requests: Optional[str] = None

    @validator("check_out_date")
    def check_out_after_check_in(cls, v, values):
        if "check_in_date" in values and v <= values["check_in_date"]:
            raise ValueError("Дата выезда должна быть позже даты въезда")
        return v