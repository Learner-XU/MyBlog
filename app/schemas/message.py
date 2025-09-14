from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class MessageBase(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    content: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True