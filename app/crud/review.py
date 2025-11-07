from sqlalchemy.orm import Session
from app.models.review import Review, ReviewStatus
from fastapi import HTTPException

def get_pending_reviews(db: Session):
    return db.query(Review).filter(Review.status == ReviewStatus.PENDING).all()

def get_review_by_id(db: Session, review_id: int):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

def update_review(db: Session, review_id: int, review_update: dict, moderator_id: int):
    db_review = get_review_by_id(db, review_id)
    if db_review.status != ReviewStatus.PENDING:
        raise HTTPException(status_code=400, detail="Review not pending")
    for key, value in review_update.items():
        setattr(db_review, key, value)
    db_review.moderated_by = moderator_id
    db.commit()
    db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int):
    db_review = get_review_by_id(db, review_id)
    db.delete(db_review)
    db.commit()