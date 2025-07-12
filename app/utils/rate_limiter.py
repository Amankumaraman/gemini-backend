from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models import Message
import os

def check_daily_limit(user_id: int, db: Session, subscription: str):
    if subscription == "Pro":
        return True  # unlimited

    limit = int(os.getenv("BASIC_DAILY_LIMIT", 5))
    today = datetime.utcnow().date()

    start_of_day = datetime(today.year, today.month, today.day)
    end_of_day = start_of_day + timedelta(days=1)

    count = (
        db.query(Message)
        .filter(
            Message.sender == "user",
            Message.created_at >= start_of_day,
            Message.created_at < end_of_day,
            Message.chatroom.has(user_id=user_id)
        )
        .count()
    )

    return count < limit
