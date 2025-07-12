from fastapi import APIRouter, Depends, Request
from app.core.deps import get_db, get_current_user
from app.services.subscription_service import create_stripe_checkout
from sqlalchemy.orm import Session
from app.db.models import User
import stripe
import os

router = APIRouter(prefix="/subscribe", tags=["subscription"])
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/pro")
def subscribe_pro(user: User = Depends(get_current_user)):
    url = create_stripe_checkout(user)
    return {"checkout_url": url}

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except Exception as e:
        return {"status": "invalid", "reason": str(e)}

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = int(session["metadata"]["user_id"])
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.subscription = "Pro"
            user.stripe_customer_id = session["customer"]
            user.stripe_subscription_id = session["subscription"]
            db.commit()

    return {"status": "success"}

@router.get("/status")
def subscription_status(user: User = Depends(get_current_user)):
    return {"subscription": user.subscription}
