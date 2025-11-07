from pydantic import BaseModel
from typing import Optional, List

class HotelBase(BaseModel):
    name: str
    description: Optional[str] = None
    country: str
    city: str
    address: str
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    manager_id: Optional[int] = None

class HotelCreate(HotelBase):
    pass

class HotelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    manager_id: Optional[int] = None

class HotelOut(HotelBase):
    id: int
    rating: float
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True