# app/models/favorite.py
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import TimestampMixin


class Favorite(Base, TimestampMixin):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)  # 'hotel' или 'location'
    entity_id = Column(Integer, nullable=False, index=True)

    user = relationship("User", back_populates="favorites", lazy="select")

    __table_args__ = (
        UniqueConstraint('user_id', 'entity_type', 'entity_id', name='uq_user_favorite'),
    )

    def __repr__(self):
        return f"<Favorite(user={self.user_id}, {self.entity_type}={self.entity_id})>"