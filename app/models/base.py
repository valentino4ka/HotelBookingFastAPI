from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class TimestampMixin:
    """Миксин для добавления временных меток"""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class SoftDeleteMixin:
    """Миксин для мягкого удаления"""
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)