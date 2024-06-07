from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from fitness_app.core.utils import NonEmptyStr


class MessageCreateSchema(BaseModel):
    chat_id: int
    content: NonEmptyStr


class MessageBaseSchema(MessageCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    sender_id: Optional[int]


class MessageSchema(MessageBaseSchema):

    id: int
    chat_id: int
    timestamp: datetime
