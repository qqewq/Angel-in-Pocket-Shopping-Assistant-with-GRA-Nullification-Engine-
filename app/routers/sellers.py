from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Seller, Product
from ..dependencies import get_current_user
from ..deal_detector import evaluate_product_safety

router = APIRouter(prefix="/sellers", tags=["sellers"])

@router.get("/{seller_id}/trust")
def seller_trust(
    seller_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    seller = db.query(Seller).get(seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    # Для расчёта доверия используем средний trust_score по всем товарам продавца
    # с учётом подписки пользователя (глубина графа)
    products = db.query(Product).filter(Product.seller_id == seller_id).all()
    if not products:
        return {"seller_id": seller_id, "average_trust": 1.0, "products_count": 0}
    trusts = []
    for p in products:
        safety = evaluate_product_safety(p.id, db, user_tier=current_user.tier.value)
        trusts.append(safety["trust_score"])
    avg_trust = round(sum(trusts) / len(trusts), 4)
    return {
        "seller_id": seller_id,
        "average_trust": avg_trust,
        "products_count": len(trusts)
    }
