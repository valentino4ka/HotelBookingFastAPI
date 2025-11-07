from pydantic import BaseModel
from typing import Optional

class HotelOut(BaseModel):
    id: int
    name: str
    city: str
    address: str
    rating: float

    class Config:
        from_attributes = True