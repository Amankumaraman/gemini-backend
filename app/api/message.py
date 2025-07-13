from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.message import MessageCreate, MessageOut
from app.db.models import Message, Chatroom
from app.core.deps import get_db, get_current_user
from app.tasks.gemini_task import send_to_groq
from app.utils.rate_limiter import check_daily_limit
from typing import List


router = APIRouter(prefix="/chatroom", tags=["messages"])



@router.post("/{chatroom_id}/message", response_model=MessageOut)
def send_message(chatroom_id: int, data: MessageCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chatroom = db.query(Chatroom).filter(Chatroom.id == chatroom_id, Chatroom.user_id == user.id).first()
    if not chatroom:
        raise HTTPException(status_code=404, detail="Chatroom not found")

    if not check_daily_limit(user.id, db, user.subscription):
        raise HTTPException(status_code=429, detail="Daily limit reached for Basic tier.")

    msg = Message(chatroom_id=chatroom_id, sender="user", content=data.content)
    db.add(msg)
    db.commit()
    db.refresh(msg)

    # Trigger async Gemini response using Redis queue
    from app.queue.redis_queue import push_task
    push_task(chatroom_id, msg.id, data.content)

    return msg



@router.get("/usage")
def usage_info(db: Session = Depends(get_db), user=Depends(get_current_user)):
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    start = datetime(today.year, today.month, today.day)
    end = start + timedelta(days=1)

    count = (
        db.query(Message)
        .filter(
            Message.sender == "user",
            Message.created_at >= start,
            Message.created_at < end,
            Message.chatroom.has(user_id=user.id)
        )
        .count()
    )
    return {"used": count, "limit": None if user.subscription == "Pro" else int(os.getenv("BASIC_DAILY_LIMIT", 5))}


@router.get("/{chatroom_id}/messages", response_model=List[MessageOut])
def get_chatroom_messages(chatroom_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chatroom = db.query(Chatroom).filter(Chatroom.id == chatroom_id, Chatroom.user_id == user.id).first()
    if not chatroom:
        raise HTTPException(status_code=404, detail="Chatroom not found")

    messages = db.query(Message).filter(Message.chatroom_id == chatroom_id).order_by(Message.created_at).all()
    return messages
