from pydantic import BaseModel, ConfigDict


class FileEntitySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    exercise_id: int
    filename: str
