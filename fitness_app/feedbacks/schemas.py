from pydantic import BaseModel, ConfigDict


class FeedbackCreateSchema(BaseModel):
    score: int


class FeedbackSchema(FeedbackCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    customer_id: int
    coach_id: int
