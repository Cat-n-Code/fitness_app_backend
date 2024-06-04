from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from fitness_app.users.schemas import UserCreateSchema


class Speciality(StrEnum):
    KIDS = "KIDS"
    ADULT = "ADULT"
    YOGA = "YOGA"


class CoachSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    speciality: Speciality
    user_id: int


class CoachCreateSchema(UserCreateSchema):
    speciality: Speciality


class CoachUpdateSchema(BaseModel):
    speciality: Speciality


class CoachSaveSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    speciality: Speciality
    user_id: int
