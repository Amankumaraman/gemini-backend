from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.schemas.chat import ChatroomCreate, ChatroomOut
from app.db.models import Chatroom
from app.core.deps import get_current_user, get_db
from app.cache.redis import get_cached_chatrooms, set_cached_chatrooms, invalidate_cached_chatrooms
import json

router = APIRouter(prefix="/chatroom", tags=["chatroom"])

@router.post("/", response_model=ChatroomOut)
def create_chatroom(data: ChatroomCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    room = Chatroom(name=data.name, user_id=user.id)
    db.add(room)
    db.commit()
    db.refresh(room)
    invalidate_cached_chatrooms(user.id)
    return room

@router.get("/", response_model=list[ChatroomOut])
def get_chatrooms(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cached = get_cached_chatrooms(user.id)
    if cached:
        return json.loads(cached)

    rooms = db.query(Chatroom).filter(Chatroom.user_id == user.id).all()
    result = [ChatroomOut.from_orm(r).dict() for r in rooms]

    # Use jsonable_encoder to handle datetime serialization
    encoded_result = jsonable_encoder(result)
    set_cached_chatrooms(user.id, json.dumps(encoded_result))

    return result

@router.get("/{chatroom_id}", response_model=ChatroomOut)
def get_chatroom(chatroom_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    room = db.query(Chatroom).filter(Chatroom.id == chatroom_id, Chatroom.user_id == user.id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Chatroom not found")
    return room
