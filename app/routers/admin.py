from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.booking import Booking
from app.models.review import Review
from app.schemas.user import UserOut, UserCreate, UserUpdate
from app.schemas.hotel import HotelOut, HotelCreate, HotelUpdate
from app.schemas.room import RoomOut, RoomCreate, RoomUpdate
from app.schemas.review import ReviewOut, ReviewUpdate
from app.schemas.booking import BookingOut
from app.crud.user import get_all_users, get_user_by_id, create_user, update_user, delete_user
from app.crud.hotel import get_hotels, get_hotel_by_id, create_hotel, update_hotel, delete_hotel
from app.crud.room import get_rooms_by_hotel, get_room_by_id, create_room, update_room, delete_room
from app.crud.review import get_pending_reviews, get_review_by_id, update_review, delete_review
from app.crud.booking import get_bookings_by_user, get_booking_by_id, create_booking, update_booking, delete_booking
from app.routers.auth import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return get_all_users(db)

@router.post("/users", response_model=UserOut)
def add_user(user: UserCreate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return create_user(db, user.dict())

@router.put("/users/{user_id}", response_model=UserOut)
def edit_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return update_user(db, user_id, user_update.dict(exclude_unset=True))

@router.delete("/users/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    delete_user(db, user_id)
    return {"message": "User deleted"}

# Аналогично для отелей
@router.get("/hotels", response_model=List[HotelOut])
def list_hotels(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return get_hotels(db)

@router.post("/hotels", response_model=HotelOut)
def add_hotel(hotel: HotelCreate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return create_hotel(db, hotel.dict(), current_admin.id)  # Админ может назначать менеджера

@router.put("/hotels/{hotel_id}", response_model=HotelOut)
def edit_hotel(hotel_id: int, hotel_update: HotelUpdate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return update_hotel(db, hotel_id, hotel_update.dict(exclude_unset=True))

@router.delete("/hotels/{hotel_id}")
def remove_hotel(hotel_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    delete_hotel(db, hotel_id)
    return {"message": "Hotel deleted"}

# Для комнат (админ может управлять любыми)
@router.get("/hotels/{hotel_id}/rooms", response_model=List[RoomOut])
def list_rooms(hotel_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return get_rooms_by_hotel(db, hotel_id)

@router.post("/hotels/{hotel_id}/rooms", response_model=RoomOut)
def add_room(hotel_id: int, room: RoomCreate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    if room.hotel_id != hotel_id:
        raise HTTPException(status_code=400, detail="Hotel ID mismatch")
    return create_room(db, room.dict())

@router.put("/rooms/{room_id}", response_model=RoomOut)
def edit_room(room_id: int, room_update: RoomUpdate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return update_room(db, room_id, room_update.dict(exclude_unset=True))

@router.delete("/rooms/{room_id}")
def remove_room(room_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    delete_room(db, room_id)
    return {"message": "Room deleted"}

# Для отзывов
@router.get("/reviews", response_model=List[ReviewOut])
def list_reviews(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return db.query(Review).all()  # Админ видит все

@router.put("/reviews/{review_id}", response_model=ReviewOut)
def moderate_review(review_id: int, review_update: ReviewUpdate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return update_review(db, review_id, review_update.dict(), current_admin.id)

@router.delete("/reviews/{review_id}")
def remove_review(review_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    delete_review(db, review_id)
    return {"message": "Review deleted"}

# Для бронирований
@router.get("/bookings", response_model=List[BookingOut])
def list_bookings(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return db.query(Booking).all()

@router.post("/bookings", response_model=BookingOut)
def add_booking(booking: BookingOut, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return create_booking(db, booking.dict())

@router.put("/bookings/{booking_id}", response_model=BookingOut)
def edit_booking(booking_id: int, booking_update: dict, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return update_booking(db, booking_id, booking_update)

@router.delete("/bookings/{booking_id}")
def remove_booking(booking_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    delete_booking(db, booking_id)
    return {"message": "Booking deleted"}