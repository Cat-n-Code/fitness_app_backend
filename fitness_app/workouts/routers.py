from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.core.dependencies import DbSession

workouts_router = APIRouter(prefix="/workouts", tags=["Тренировки"])


@workouts_router.post(
    "",
    response_model=WorkoutSchema,
    summary="Создание тренировки",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def create(
    session: DbSession,
    service: WorkoutServiceDep,
    user: AuthenticateUser,
    schema: WorkoutCreateSchema,
) -> WorkoutSchema:
    return await service.create(session, user, schema)


@workouts_router.get(
    "/{id}",
    response_model=WorkoutSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Тренировки с указанным id не найдено"
        }
    },
    summary="Получение тренировки по id",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_by_id(
    session: DbSession,
    service: WorkoutServiceDep,
    user: AuthenticateUser,
    id: Annotated[int, Path],
) -> WorkoutSchema:
    return await service.get_by_id(session, user, id)


@workouts_router.get(
    "/customers/{customer_id}",
    response_model=list[WorkoutSchema],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Клиента с указанным id не найдено"}
    },
    summary="Получить список тренировок клиента",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_workouts_by_customer_id(
    session: DbSession,
    user: AuthenticateUser,
    customer_id: Annotated[int, Path],
) -> WorkoutSchema:
    return await service.get_workouts_by_customer_id(session, user, customer_id)


@workouts_router.get(
    "/users/current",
    response_model=list[WorkoutSchema],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Тренировки с указанным id не найдено"
        }
    },
    summary="Получение тренировок текущего пользователя",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_by_user_id(
    session: DbSession,
    service: WorkoutServiceDep,
    user: AuthenticateUser,
    page: PageField = 0,
    size: SizeField = 10,
) -> list[WorkoutSchema]:
    return await service.get_by_user_id(session, user.id, page, size)
