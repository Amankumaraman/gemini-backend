import stripe
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.db.models import User

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
DOMAIN = os.getenv("DOMAIN")

def create_stripe_checkout(user: User) -> str:
    checkout_session = stripe.checkout.Session.create(
        customer_email=user.mobile + "@example.com",  # for demo purposes
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "Gemini Pro Subscription",
                },
                "unit_amount": 999,  # $9.99
                "recurring": {"interval": "month"},
            },
            "quantity": 1,
        }],
        mode="subscription",
        success_url=f"{DOMAIN}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{DOMAIN}/cancel",
        metadata={"user_id": str(user.id)}
    )
    return checkout_session.url
