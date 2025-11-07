from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.room import RoomOut, RoomSearch
from app.crud.room import search_rooms

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.get("/search", response_model=List[RoomOut])
def search_available_rooms(
    city: str = Query(..., description="Город для поиска отелей"),
    check_in_date: str = Query(..., description="Дата въезда (YYYY-MM-DD)"),
    check_out_date: str = Query(..., description="Дата выезда (YYYY-MM-DD)"),
    price_min: Optional[float] = Query(None, description="Минимальная цена за ночь"),
    price_max: Optional[float] = Query(None, description="Максимальная цена за ночь"),
    max_guests: Optional[int] = Query(None, description="Минимальное количество гостей"),
    amenities: Optional[str] = Query(None, description="Список удобств, разделенных запятой (e.g., Wi-Fi,Парковка)"),
    db: Session = Depends(get_db)
):
    """
    Поиск свободных комнат по параметрам.
    - Обязательные: city, check_in_date, check_out_date.
    - Amenities: строка с именами, разделенными запятой.
    """
    # Парсим amenities в список
    amenities_list = [a.strip() for a in amenities.split(",")] if amenities else None
    
    # Создаем объект поиска (Pydantic валидирует даты)
    search_params = RoomSearch(
        city=city,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        price_min=price_min,
        price_max=price_max,
        max_guests=max_guests,
        amenities=amenities_list
    )
    
    rooms = search_rooms(
        db=db,
        city=search_params.city,
        check_in_date=search_params.check_in_date,
        check_out_date=search_params.check_out_date,
        price_min=search_params.price_min,
        price_max=search_params.price_max,
        max_guests=search_params.max_guests,
        amenities=search_params.amenities
    )
    return rooms