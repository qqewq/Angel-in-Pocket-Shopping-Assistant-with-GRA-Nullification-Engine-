from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Product
from ..dependencies import get_current_user, require_subscription
from ..deal_detector import evaluate_product_safety

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/{product_id}/safety")
def product_safety(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    tier = current_user.tier.value
    if tier == "free":
        raise HTTPException(status_code=402, detail="Upgrade subscription to access safety scores")
    return evaluate_product_safety(product_id, db, user_tier=tier)
