from sqlalchemy.orm import Session, joinedload
from app.models.hotel import Hotel
from fastapi import HTTPException

def get_hotels(db: Session, manager_id: int = None):
    query = db.query(Hotel).options(joinedload(Hotel.rooms), joinedload(Hotel.reviews))
    if manager_id:
        query = query.filter(Hotel.manager_id == manager_id)
    return query.all()

def get_hotel_by_id(db: Session, hotel_id: int, manager_id: int = None):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    if manager_id and hotel.manager_id != manager_id:
        raise HTTPException(status_code=403, detail="Not your hotel")
    return hotel

def create_hotel(db: Session, hotel_create: dict, manager_id: int):
    db_hotel = Hotel(**hotel_create, manager_id=manager_id)
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def update_hotel(db: Session, hotel_id: int, hotel_update: dict, manager_id: int = None):
    db_hotel = get_hotel_by_id(db, hotel_id, manager_id)
    for key, value in hotel_update.items():
        if value is not None:
            setattr(db_hotel, key, value)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def delete_hotel(db: Session, hotel_id: int, manager_id: int = None):
    db_hotel = get_hotel_by_id(db, hotel_id, manager_id)
    db.delete(db_hotel)
    db.commit()