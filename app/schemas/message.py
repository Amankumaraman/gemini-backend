from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    content: str


class MessageOut(BaseModel):
    id: int
    chatroom_id: int
    sender: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
