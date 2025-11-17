# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Импортируем Base и ВСЕ модели явно ЗДЕСЬ, а не в __init__.py
from app.database import Base
import os
from dotenv import load_dotenv

load_dotenv()

# Подтягиваем ВСЕ модели явно — это важно!
# Если пропустишь хоть одну — автогенерация её не увидит
from app.models.user import User, UserRole
from app.models.amenity import Amenity, hotel_amenities, room_amenities
from app.models.hotel import Hotel
from app.models.room import Room, RoomType, BedType
from app.models.booking import Booking, BookingStatus, PaymentStatus
from app.models.review import Review, ReviewStatus
from app.models.audit_log import AuditLog, ActionType
from app.models.location_category import LocationCategory
from app.models.location import Location
from app.models.location_photo import LocationPhoto
from app.models.favorite import Favorite
from app.models.event import Event
from app.models.notification import Notification

# Если добавишь ещё модели — просто допиши их сюда

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Подмена URL из .env
if os.getenv("DATABASE_URL"):
    config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()