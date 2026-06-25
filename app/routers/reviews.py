from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Review, Product
from ..dependencies import get_current_user

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/")
def create_review(
    product_id: int,
    rating: float,
    text: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    review = Review(
        text=text,
        rating=rating,
        author_id=current_user.id,
        product_id=product_id,
        sentiment_score=0.0  # Заглушка, должно вычисляться NLP-моделью
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return {"id": review.id, "created_at": review.created_at}
