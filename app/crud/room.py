from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload
from app.models.room import Room
from app.models.hotel import Hotel
from app.models.booking import Booking, BookingStatus
from app.models.amenity import Amenity, room_amenities
from datetime import date
from typing import List, Optional
from fastapi import HTTPException

def search_rooms(
    db: Session,
    city: str,
    check_in_date: date,
    check_out_date: date,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    max_guests: Optional[int] = None,
    amenities: Optional[List[str]] = None
) -> List[Room]:
    if check_in_date >= check_out_date:
        raise HTTPException(status_code=400, detail="Дата въезда должна быть раньше даты выезда")

    active_statuses = [BookingStatus.PENDING, BookingStatus.CONFIRMED, BookingStatus.CHECKED_IN]
    booked_subquery = (
        db.query(Booking.room_id, func.count(Booking.id).label("booked_count"))
        .filter(
            Booking.booking_status.in_(active_statuses),
            or_(
                (Booking.check_in_date < check_out_date) & (Booking.check_out_date > check_in_date)
            )
        )
        .group_by(Booking.room_id)
        .subquery()
    )

    query = (
        db.query(Room)
        .join(Hotel, Room.hotel_id == Hotel.id)
        .outerjoin(booked_subquery, Room.id == booked_subquery.c.room_id)
        .options(joinedload(Room.hotel))
        .filter(
            func.lower(Hotel.city) == city.lower(),
            Room.is_available == True,
            Room.quantity > func.coalesce(booked_subquery.c.booked_count, 0)
        )
    )

    if price_min is not None:
        query = query.filter(Room.price_per_night >= price_min)
    if price_max is not None:
        query = query.filter(Room.price_per_night <= price_max)
    if max_guests is not None:
        query = query.filter(Room.max_guests >= max_guests)
    if amenities:
        query = query.join(room_amenities, Room.id == room_amenities.c.room_id)
        query = query.join(Amenity, Amenity.id == room_amenities.c.amenity_id)
        query = query.filter(Amenity.name.in_(amenities))
        query = query.group_by(Room.id)
        query = query.having(func.count(Amenity.id.distinct()) == len(amenities))

    return query.all()

# Новые CRUD для комнат
def get_rooms_by_hotel(db: Session, hotel_id: int):
    return db.query(Room).filter(Room.hotel_id == hotel_id).all()

def get_room_by_id(db: Session, room_id: int, hotel_id: int = None):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if hotel_id and room.hotel_id != hotel_id:
        raise HTTPException(status_code=403, detail="Not in your hotel")
    return room

def create_room(db: Session, room_create: dict):
    db_room = Room(**room_create)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room(db: Session, room_id: int, room_update: dict, hotel_id: int = None):
    db_room = get_room_by_id(db, room_id, hotel_id)
    for key, value in room_update.items():
        if value is not None:
            setattr(db_room, key, value)
    db.commit()
    db.refresh(db_room)
    return db_room

def delete_room(db: Session, room_id: int, hotel_id: int = None):
    db_room = get_room_by_id(db, room_id, hotel_id)
    db.delete(db_room)
    db.commit()