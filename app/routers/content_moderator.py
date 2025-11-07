from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.review import ReviewOut, ReviewUpdate
from app.crud.review import get_pending_reviews, update_review
from app.routers.auth import get_current_content_moderator
from app.models.user import User, UserRole


router = APIRouter(tags=["content_moderator"])

@router.get("/reviews/pending", response_model=List[ReviewOut])
def list_pending_reviews(db: Session = Depends(get_db), current_moderator: User = Depends(get_current_content_moderator)):
    return get_pending_reviews(db)

@router.put("/reviews/{review_id}", response_model=ReviewOut)
def moderate_review(review_id: int, review_update: ReviewUpdate, db: Session = Depends(get_db), current_moderator: User = Depends(get_current_content_moderator)):
    return update_review(db, review_id, review_update.dict(), current_moderator.id)