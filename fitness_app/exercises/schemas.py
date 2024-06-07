from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, ConfigDict

from fitness_app.file_entities.schemas import FileEntitySchema


class ExerciseType(StrEnum):
    BASIC = "Базовое"
    INSULATING = "Изолирующее"


class Difficulty(StrEnum):
    BEGINNER = "Начинающий"
    AVERAGE = "Средний"
    PROFESSIONAL = "Профессионал"


class ExerciseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    originalUri: Optional[str] = None
    name: str
    muscle: Optional[str] = None
    additionalMuscle: Optional[str] = None
    type: Optional[ExerciseType] = None
    equipment: Optional[str] = None
    difficulty: Optional[Difficulty] = None
    photos: Optional[list[FileEntitySchema]] = None
    description: Optional[str] = None


class ExerciseCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    originalUri: Optional[str] = None
    name: str
    muscle: Optional[str] = None
    additionalMuscle: Optional[str] = None
    type: Optional[ExerciseType] = None
    equipment: Optional[str] = None
    difficulty: Optional[Difficulty] = None
    description: Optional[str] = None


class ExerciseUpdateSchema(BaseModel):
    id: int
    originalUri: Optional[str] = None
    name: str
    muscle: Optional[str] = None
    additionalMuscle: Optional[str] = None
    type: Optional[ExerciseType] = None
    equipment: Optional[str] = None
    difficulty: Optional[Difficulty] = None
    description: Optional[str] = None
