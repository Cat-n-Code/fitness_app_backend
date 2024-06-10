from datetime import date
from typing import List

from fastapi import APIRouter, Depends, status

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.core.dependencies import DbSession, StepsServiceDep
from fitness_app.steps.schemas import StepsCreateSchema, StepsSchema

steps_router = APIRouter(prefix="/steps", tags=["Steps"])


@steps_router.get(
    "",
    summary="Get steps for a specific period",
    response_model=List[StepsSchema],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The steps with given dates was not found"
        },
    },
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_steps_by_dates(
    session: DbSession,
    service: StepsServiceDep,
    user: AuthenticateUser,
    date_start: date,
    date_finish: date,
):
    steps = await service.get_by_dates(session, user.id, date_start, date_finish)
    validated_steps = [StepsSchema.model_validate(step) for step in steps]
    return validated_steps


@steps_router.put(
    "",
    summary="Create today steps",
    response_model=StepsSchema,
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def create_or_update_steps(
    session: DbSession,
    service: StepsServiceDep,
    user: AuthenticateUser,
    schema: StepsCreateSchema,
):
    step = await service.create_or_update(session, user.id, schema)
    return StepsSchema.model_validate(step)
