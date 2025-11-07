from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from app.schemas.hotel import HotelOut  # Будет создан ниже

class RoomBase(BaseModel):
    name: str
    room_type: str
    description: Optional[str] = None
    size_sqm: Optional[float] = None
    max_guests: int
    num_beds: int
    bed_type: str
    price_per_night: float
    quantity: int

class RoomSearch(BaseModel):
    city: str
    check_in_date: date
    check_out_date: date
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    max_guests: Optional[int] = None
    amenities: Optional[List[str]] = None  # Список имен удобств

class RoomOut(RoomBase):
    id: int
    hotel: HotelOut  # Вложенная информация об отеле

    class Config:
        from_attributes = True