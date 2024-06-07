from datetime import datetime

from pydantic import BaseModel, ConfigDict

from fitness_app.core.utils import NonEmptyStr


class MessageCreateSchema(BaseModel):
    content: NonEmptyStr


class MessageBaseSchema(MessageCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    chat_id: int
    sender_id: int


class MessageSchema(MessageBaseSchema):

    id: int
    timestamp: datetime
