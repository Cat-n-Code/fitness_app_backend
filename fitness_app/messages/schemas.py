from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MessageCreateSchema(BaseModel):
    content: Optional[str] = None
    files: list[str] = []
    voice: Optional[str] = None


class MessageBaseSchema(MessageCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    chat_id: int
    sender_id: int


class MessageUpdateSchema(MessageCreateSchema):
    id: int


class MessageSchema(MessageBaseSchema):
    id: int
    timestamp: datetime
