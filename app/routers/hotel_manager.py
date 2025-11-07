from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.hotel import HotelOut, HotelUpdate
from app.schemas.room import RoomOut, RoomCreate, RoomUpdate
from app.crud.hotel import get_hotel_by_id, get_hotels, update_hotel, delete_hotel
from app.crud.room import get_room_by_id, get_rooms_by_hotel, create_room, update_room, delete_room
from app.routers.auth import get_current_hotel_manager
from app.models.user import User

router = APIRouter(tags=["hotel_manager"])

@router.get("/hotels", response_model=List[HotelOut])
def list_my_hotels(db: Session = Depends(get_db), current_manager: User = Depends(get_current_hotel_manager)):
    return get_hotels(db, current_manager.id)

@router.put("/hotels/{hotel_id}", response_model=HotelOut)
def edit_hotel(hotel_id: int, hotel_update: HotelUpdate, db: Session = Depends(get_db), current_manager: User = Depends(get_current_hotel_manager)):
    return update_hotel(db, hotel_id, hotel_update.dict(exclude_unset=True), current_manager.id)

@router.delete("/hotels/{hotel_id}")
def remove_hotel(hotel_id: int, db: Session = Depends(get_db), current_manager: User = Depends(get_current_hotel_manager)):
    delete_hotel(db, hotel_id, current_manager.id)
    return {"message": "Hotel deleted"}

@router.get("/hotels/{hotel_id}/rooms", response_model=List[RoomOut])
def list_rooms(hotel_id: int, db: Session = Depends(get_db), current_manager: User = Depends(get_current_hotel_manager)):
    get_hotel_by_id(db, hotel_id, current_manager.id)  # Проверка владения
    return get_rooms_by_hotel(db, hotel_id)

@router.post("/hotels/{hotel_id}/rooms", response_model=RoomOut)
def add_room(hotel_id: int, room: RoomCreate, db: Session = Depends(get_db), current_manager: User = Depends(get_current_hotel_manager)):
    get_hotel_by_id(db, hotel_id, current_manager.id)
    if room.hotel_id != hotel_id:
        raise HTTPException(status_code=400, detail="Hotel ID mismatch")
    return create_room(db, room.dict())

@router.put("/rooms/{room_id}", response_model=RoomOut)
def edit_room(room_id: int, room_update: RoomUpdate, db: Session = Depends(get_db), current_manager: User = Depends(get_current_hotel_manager)):
    room = get_room_by_id(db, room_id)
    get_hotel_by_id(db, room.hotel_id, current_manager.id)  # Проверка
    return update_room(db, room_id, room_update.dict(exclude_unset=True))

@router.delete("/rooms/{room_id}")
def remove_room(room_id: int, db: Session = Depends(get_db), current_manager: User = Depends(get_current_hotel_manager)):
    room = get_room_by_id(db, room_id)
    get_hotel_by_id(db, room.hotel_id, current_manager.id)
    delete_room(db, room_id)
    return {"message": "Room deleted"}