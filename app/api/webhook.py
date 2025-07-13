# app/api/webhook.py
from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse
import stripe
import os
from dotenv import load_dotenv
from app.db.database import SessionLocal
from app.db.models import User

load_dotenv()
router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return JSONResponse(status_code=400, content={"error": "Invalid signature"})

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        subscription_id = session["subscription"]

        subscription = stripe.Subscription.retrieve(subscription_id)
        user_id = subscription["metadata"].get("user_id")

        if user_id:
            db = SessionLocal()
            user = db.query(User).filter(User.id == int(user_id)).first()
            if user:
                user.subscription = "Pro"
                db.commit()
                db.close()

    return JSONResponse(status_code=200, content={"status": "success"})
