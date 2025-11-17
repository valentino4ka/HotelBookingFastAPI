# app/models/__init__.py
# Этот файл теперь нужен ТОЛЬКО для работы приложения (не для Alembic!)

from app.database import Base

# Импортируем ВСЕ модели явно — это заставит SQLAlchemy их "увидеть"
from app.models import user
from app.models import hotel
from app.models import room
from app.models import booking
from app.models import review
from app.models import amenity
from app.models import audit_log
from app.models import location_category
from app.models import location
from app.models import location_photo
from app.models import favorite
from app.models import event
from app.models import notification

# Ничего больше не экспортируем — главное, что они импортированы