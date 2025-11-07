from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
import enum
from app.database import Base
from app.models.base import TimestampMixin, SoftDeleteMixin


class ReviewStatus(str, enum.Enum):
    """Статусы отзыва"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Review(Base, TimestampMixin, SoftDeleteMixin):
    """Модель отзыва"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True, index=True)
    
    overall_rating = Column(Float, nullable=False)
    cleanliness_rating = Column(Float, nullable=True)
    location_rating = Column(Float, nullable=True)
    service_rating = Column(Float, nullable=True)
    value_rating = Column(Float, nullable=True)
    amenities_rating = Column(Float, nullable=True)
    
    title = Column(String(255), nullable=True)
    comment = Column(Text, nullable=False)
    
    status = Column(
        SQLEnum(ReviewStatus),
        default=ReviewStatus.PENDING,
        nullable=False,
        index=True
    )
    moderated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    moderation_comment = Column(Text, nullable=True)
    
    helpful_count = Column(Integer, default=0, nullable=False)
    not_helpful_count = Column(Integer, default=0, nullable=False)
    
    hotel_response = Column(Text, nullable=True)
    response_date = Column(DateTime(timezone=True), nullable=True)  # ← ИСПРАВЛЕНО
    
    user = relationship(
        "User",
        back_populates="reviews",
        lazy="select",
        foreign_keys=[user_id]
    )
    
    hotel = relationship(
        "Hotel",
        back_populates="reviews",
        lazy="select"
    )
    
    moderator = relationship(
        "User",
        back_populates="moderated_reviews",
        lazy="select",
        foreign_keys=[moderated_by]
    )

    def __repr__(self):
        return f"<Review(id={self.id}, hotel_id={self.hotel_id}, rating={self.overall_rating}, status={self.status})>"