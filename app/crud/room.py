from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload
from app.models.room import Room
from app.models.hotel import Hotel
from app.models.booking import Booking, BookingStatus
from app.models.amenity import Amenity, room_amenities
from datetime import date
from typing import List, Optional
from fastapi import HTTPException  # Добавлено для валидации дат

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
    """
    Поиск свободных комнат с фильтрами.
    - Фильтрует по городу отеля (case-insensitive).
    - Проверяет доступность: quantity > кол-во активных бронирований, пересекающихся с датами.
    - Применяет опциональные фильтры по цене, гостям, удобствам.
    """
    # Простая валидация дат (чтобы избежать бессмысленных запросов)
    if check_in_date >= check_out_date:
        raise HTTPException(status_code=400, detail="Дата въезда должна быть раньше даты выезда")

    # Подзапрос для подсчета забронированных комнат на даты
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

    # Основной запрос (убрали aliased для единого алиаса subquery)
    query = (
        db.query(Room)
        .join(Hotel, Room.hotel_id == Hotel.id)
        .outerjoin(booked_subquery, Room.id == booked_subquery.c.room_id)
        .options(joinedload(Room.hotel))  # Загружаем отель для вывода
        .filter(
            func.lower(Hotel.city) == city.lower(),
            Room.is_available == True,
            # Свободные: quantity > booked_count (или 0 если нет бронирований)
            Room.quantity > func.coalesce(booked_subquery.c.booked_count, 0)
        )
    )

    # Фильтры
    if price_min is not None:
        query = query.filter(Room.price_per_night >= price_min)
    if price_max is not None:
        query = query.filter(Room.price_per_night <= price_max)
    if max_guests is not None:
        query = query.filter(Room.max_guests >= max_guests)
    if amenities:
        # JOIN с amenities через secondary table
        query = query.join(room_amenities, Room.id == room_amenities.c.room_id)
        query = query.join(Amenity, Amenity.id == room_amenities.c.amenity_id)
        query = query.filter(Amenity.name.in_(amenities))
        query = query.group_by(Room.id)
        query = query.having(func.count(Amenity.id.distinct()) == len(amenities))  # Все указанные amenities

    return query.all()