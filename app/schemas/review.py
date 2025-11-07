from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.review import ReviewStatus

class ReviewBase(BaseModel):
    overall_rating: float
    comment: str
    # Другие рейтинги опционально

class ReviewOut(BaseModel):
    id: int
    user_id: int
    hotel_id: int
    overall_rating: float
    comment: str
    status: ReviewStatus
    created_at: datetime

    class Config:
        from_attributes = True

class ReviewUpdate(BaseModel):
    status: ReviewStatus
    moderation_comment: Optional[str] = None