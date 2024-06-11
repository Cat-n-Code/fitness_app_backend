from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class Feeling(StrEnum):
    GOOD = "GOOD"
    NORMAL = "NORMAL"
    BAD = "BAD"


class DiarySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    feeling: Feeling
    date_field: date


class DiaryCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    feeling: Feeling
