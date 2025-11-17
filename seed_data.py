"""
Скрипт для заполнения базы данных тестовыми данными
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, UserRole, Amenity, Hotel, Room, RoomType, BedType
from app.crud.user import hash_password


def seed_users(db: Session):
    """Создание тестовых пользователей"""
    users = [
        User(
            email="admin@hotel.ru",
            username="admin",
            hashed_password=hash_password("admin123"),
            first_name="Админ",
            last_name="Системы",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True
        ),
        User(
            email="manager@otel.ru",
            username="manager",
            hashed_password=hash_password("manager123"),
            first_name="Менеджер",
            last_name="Отеля",
            role=UserRole.HOTEL_MANAGER,
            is_active=True,
            is_verified=True
        ),
        User(
            email="moderator@hotel.ru",
            username="moderator",
            hashed_password=hash_password("moderator123"),
            first_name="Модератор",
            last_name="Контента",
            role=UserRole.CONTENT_MODERATOR,
            is_active=True,
            is_verified=True
        ),
        User(
            email="user@example.ru",
            username="testuser",
            hashed_password=hash_password("user123"),
            first_name="Иван",
            last_name="Петров",
            role=UserRole.USER,
            is_active=True,
            is_verified=True
        ),
    ]

    for user in users:
        db.add(user)

    db.commit()
    print("Пользователи созданы")


def seed_amenities(db: Session):
    """Создание удобств"""
    amenities = [
        Amenity(name="Wi-Fi", category="general", icon="wifi"),
        Amenity(name="Парковка", category="general", icon="parking"),
        Amenity(name="Бассейн", category="general", icon="pool"),
        Amenity(name="Фитнес-зал", category="general", icon="gym"),
        Amenity(name="Ресторан", category="general", icon="restaurant"),
        Amenity(name="Бар", category="general", icon="bar"),
        Amenity(name="Спа", category="general", icon="spa"),
        Amenity(name="Круглосуточная стойка регистрации", category="general", icon="reception"),

        Amenity(name="Кондиционер", category="room", icon="ac"),
        Amenity(name="Телевизор", category="room", icon="tv"),
        Amenity(name="Мини-бар", category="room", icon="minibar"),
        Amenity(name="Сейф", category="room", icon="safe"),
        Amenity(name="Балкон", category="room", icon="balcony"),
        Amenity(name="Рабочий стол", category="room", icon="desk"),

        Amenity(name="Фен", category="bathroom", icon="hairdryer"),
        Amenity(name="Ванна", category="bathroom", icon="bathtub"),
        Amenity(name="Душ", category="bathroom", icon="shower"),

        Amenity(name="Кухня", category="kitchen", icon="kitchen"),
        Amenity(name="Микроволновка", category="kitchen", icon="microwave"),
        Amenity(name="Холодильник", category="kitchen", icon="fridge"),
    ]

    for amenity in amenities:
        db.add(amenity)

    db.commit()
    print("Удобства созданы")


def seed_hotels(db: Session):
    """Создание тестовых отелей"""
    manager = db.query(User).filter(User.role == UserRole.HOTEL_MANAGER).first()
    manager_id = manager.id if manager else None

    hotels = [
        Hotel(
            name="Гранд Плаза Москва",
            description="Роскошный 5-звёздочный отель в центре столицы",
            country="Россия",
            city="Москва",
            address="ул. Тверская, д. 10",
            postal_code="125009",
            latitude=55.7589,
            longitude=37.6140,
            phone="+7-495-123-45-67",
            email="info@grandplaza.ru",
            manager_id=manager_id,
            is_active=True,
            is_verified=True,
            rating=4.7,
            total_reviews=98
        ),
        Hotel(
            name="Морской Бриз",
            description="Уютный курортный отель на берегу Чёрного моря",
            country="Россия",
            city="Сочи",
            address="ул. Морская, д. 25",
            postal_code="354000",
            latitude=43.6028,
            longitude=39.7342,
            phone="+7-862-555-88-99",
            email="info@morskoibriz.ru",
            manager_id=manager_id,
            is_active=True,
            is_verified=True,
            rating=4.9,
            total_reviews=72
        ),
    ]

    for hotel in hotels:
        db.add(hotel)

    db.commit()
    print("Отели созданы")


def seed_rooms(db: Session):
    """Создание тестовых номеров"""
    hotels = db.query(Hotel).all()
    if not hotels:
        print("Нет отелей — номера не создаются.")
        return

    for hotel in hotels:
        rooms = [
            Room(
                hotel_id=hotel.id,
                name="Стандартный двухместный",
                room_type=RoomType.DOUBLE,
                description="Уютный номер с двуспальной кроватью",
                size_sqm=28.0,
                max_guests=2,
                num_beds=1,
                bed_type=BedType.DOUBLE,
                price_per_night=7500.0,
                is_available=True,
                quantity=15
            ),
            Room(
                hotel_id=hotel.id,
                name="Люкс с видом на море",
                room_type=RoomType.SUITE,
                description="Просторный люкс с панорамным видом и зоной отдыха",
                size_sqm=65.0,
                max_guests=4,
                num_beds=2,
                bed_type=BedType.KING,
                price_per_night=18500.0,
                is_available=True,
                quantity=3
            ),
        ]
        for room in rooms:
            db.add(room)

    db.commit()
    print("Номера созданы")


def seed_all():
    db = SessionLocal()
    try:
        print("Начинаем заполнение базы...")
        seed_users(db)
        seed_amenities(db)
        seed_hotels(db)
        seed_rooms(db)
        print("\nБаза успешно заполнена тестовыми данными!")
    except Exception as e:
        print(f"\nОшибка: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()