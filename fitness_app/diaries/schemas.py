from datetime import date

from pydantic import BaseModel, ConfigDict

from fitness_app.diaries.models import Feeling


class DiarySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    feeling: Feeling
    date_field: date


class DiaryCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    feeling: Feeling
