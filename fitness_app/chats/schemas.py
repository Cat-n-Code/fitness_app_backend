from datetime import datetime

from pydantic import BaseModel, ConfigDict

from fitness_app.users.schemas import UserSchema


class ChatSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    users: list[UserSchema]
    last_timestamp: datetime
