from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ChatroomCreate(BaseModel):
    name: str

class ChatroomOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
