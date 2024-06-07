from fastapi import APIRouter, Depends

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import IsCoach
from fitness_app.coaches.models import Coach
from fitness_app.coaches.schemas import (
    CoachCreateSchema,
    CoachSchema,
    CoachUpdateSchema,
)
from fitness_app.core.dependencies import CoachServiceDep, DbSession
from fitness_app.core.schemas import PageSchema
from fitness_app.core.utils import IdField, PageField, SizeField

coaches_router = APIRouter(prefix="/coaches", tags=["Тренеры"])


@coaches_router.get(
    "/",
    summary="Получить список всех тренеров",
    response_model=PageSchema,
    # dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_all(
    session: DbSession,
    service: CoachServiceDep,
    page: PageField = 0,
    size: SizeField = 10,
):
    coaches = await service.get_all(session, page, size)
    return PageSchema(
        total_items_count=coaches.total_items_count,
        items=list(map(CoachSchema.model_validate, coaches.items)),
    )


@coaches_router.post(
    "/registration",
    summary="Создать тренера",
    response_model=CoachSchema,
    # dependencies=[Depends(HasPermission(Anonymous()))],
)
async def create(
    session: DbSession,
    service: CoachServiceDep,
    schema: CoachCreateSchema,
):
    coach = await service.create(session, schema)
    return CoachSchema.model_validate(coach, from_attributes=True)


@coaches_router.get(
    "/current",
    summary="Получить текущего авторизованного тренера",
    response_model=CoachSchema,
    dependencies=[Depends(HasPermission(IsCoach()))],
)
async def get_current(
    service: CoachServiceDep,
    user: AuthenticateUser,
):
    coach = await service.get_current(user)
    return CoachSchema.model_validate(coach)


@coaches_router.put(
    "/current",
    summary="Обновить текущего авторизованного тренера",
    response_model=CoachSchema,
    dependencies=[Depends(HasPermission(IsCoach()))],
)
async def update_current(
    session: DbSession,
    service: CoachServiceDep,
    user: AuthenticateUser,
    schema: CoachUpdateSchema,
) -> Coach:
    coach = await service.update_by_user(session, schema, user)
    return CoachSchema.model_validate(coach)


@coaches_router.get(
    "/my_customers",
    response_model=PageSchema,
    summary="Получение своих тренеров",
    dependencies=[Depends(HasPermission(IsCoach()))],
)
async def get_coaches(
    user: AuthenticateUser,
    service: CoachServiceDep,
    session: DbSession,
    page: PageField = 0,
    size: SizeField = 10,
):
    customers = await service.get_customers_by_user(session, user, page, size)
    return PageSchema(
        total_items_count=customers.total_items_count,
        items=customers,
    )


@coaches_router.post(
    "/assign_me_customer/{customer_id}",
    response_model=CoachSchema,
    summary="Назначение клиента текущему тренеру",
    dependencies=[Depends(HasPermission(IsCoach()))],
)
async def assign_coach(
    user: AuthenticateUser,
    service: CoachServiceDep,
    session: DbSession,
    customer_id: IdField,
):
    coach = await service.assign_customer(session, user, customer_id)
    return CoachSchema.model_validate(coach)


@coaches_router.post(
    "/unassign_my_customer/{customer_id}",
    response_model=CoachSchema,
    summary="Отвязка текущего тренера от клиента",
    dependencies=[Depends(HasPermission(IsCoach()))],
)
async def unassign_coach(
    user: AuthenticateUser,
    service: CoachServiceDep,
    session: DbSession,
    customer_id: IdField,
):
    coach = await service.unassign_customer(session, user, customer_id)
    return CoachSchema.model_validate(coach)
