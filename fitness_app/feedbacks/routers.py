from fastapi import APIRouter, Depends

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import IsCustomer
from fitness_app.core.dependencies import CustomerServiceDep, DbSession
from fitness_app.core.utils import IdField
from fitness_app.feedbacks.schemas import FeedbackCreateSchema, FeedbackSchema

customers_router = APIRouter(prefix="/customers", tags=["Клиенты"])


@customers_router.post(
    "/{coach_id}",
    summary="Создать клиента",
    response_model=FeedbackSchema,
    dependencies=[Depends(HasPermission(IsCustomer))],
)
async def create(
    session: DbSession,
    service: CustomerServiceDep,
    user: AuthenticateUser,
    schema: FeedbackCreateSchema,
    coach_id: IdField,
):
    feedback = await service.create(session, schema)
    return FeedbackSchema.model_validate(feedback, from_attributes=True)
