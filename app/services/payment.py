import stripe
from sqlalchemy.orm import Session
from ..config import settings
from ..models import User, SubscriptionTier

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(user: User, plan: str, plan_info: dict):
    if not user.stripe_customer_id:
        customer = stripe.Customer.create(email=user.email)
        user.stripe_customer_id = customer.id
        # Обновление в БД произойдёт в вызывающем коде
    session = stripe.checkout.Session.create(
        customer=user.stripe_customer_id,
        payment_method_types=["card"],
        line_items=[{
            "price": plan_info["price_id"],
            "quantity": 1,
        }],
        mode="subscription",
        success_url="https://yourapp.com/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://yourapp.com/cancel",
    )
    return session.url

def handle_webhook_event(event, db: Session):
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_id = session["customer"]
        user = db.query(User).filter_by(stripe_customer_id=customer_id).first()
        if not user:
            return
        # Определяем план (в реальном проекте – из line_items или metadata)
        # Здесь устанавливаем basic по умолчанию, но можно улучшить
        user.tier = SubscriptionTier.basic
        db.commit()
    elif event["type"] == "customer.subscription.deleted":
        sub = event["data"]["object"]
        customer_id = sub["customer"]
        user = db.query(User).filter_by(stripe_customer_id=customer_id).first()
        if user:
            user.tier = SubscriptionTier.free
            db.commit()
