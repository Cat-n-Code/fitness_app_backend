from fastapi import APIRouter, Depends

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.coaches.models import Coach
from fitness_app.coaches.schemas import (
    CoachCreateSchema,
    CoachSchema,
    CoachUpdateSchema,
)
from fitness_app.core.dependencies import CoachServiceDep, DbSession

coaches_router = APIRouter(prefix="/coaches", tags=["Тренеры"])


@coaches_router.post(
    "/",
    summary="Создать тренера",
    response_model=CoachSchema,
    # dependencies=[Depends(HasPermission(Authenticated()))],
)
async def create(
    session: DbSession,
    service: CoachServiceDep,
    schema: CoachCreateSchema,
) -> Coach:
    coach = await service.create(session, schema)
    return CoachSchema.model_validate(coach, from_attributes=True)


@coaches_router.get(
    "/current",
    summary="Получить текущего авторизованного тренера",
    response_model=CoachSchema,
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_current(
    session: DbSession,
    service: CoachServiceDep,
    user: AuthenticateUser,
):
    coach = await service.get_current(user)
    return CoachSchema.model_validate(coach)


@coaches_router.put(
    "/current",
    summary="Обновить текущего авторизованного тренера",
    response_model=CoachSchema,
    # dependencies=[Depends(HasPermission(Authenticated()))],
)
async def update_current(
    session: DbSession,
    service: CoachServiceDep,
    user: AuthenticateUser,
    schema: CoachUpdateSchema,
) -> Coach:
    coach = await service.update_by_user(session, schema, user)
    return CoachSchema.model_validate(coach)
