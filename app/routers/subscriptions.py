import stripe
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from ..config import settings
from ..database import get_db
from ..models import User, SubscriptionTier
from ..dependencies import get_current_user
from ..services.payment import create_checkout_session, handle_webhook_event

stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

PLANS = {
    "basic": {"price_id": "price_basic_id", "tier": SubscriptionTier.basic},
    "premium": {"price_id": "price_premium_id", "tier": SubscriptionTier.premium},
    "enterprise": {"price_id": "price_enterprise_id", "tier": SubscriptionTier.enterprise},
}

@router.post("/create-checkout-session")
def create_subscription_session(
    plan: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if plan not in PLANS:
        raise HTTPException(status_code=400, detail="Invalid plan")
    if current_user.tier != SubscriptionTier.free:
        raise HTTPException(status_code=400, detail="Already subscribed")
    session_url = create_checkout_session(current_user, plan, PLANS[plan])
    return {"checkout_url": session_url}

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    handle_webhook_event(event, db)
    return {"status": "success"}
