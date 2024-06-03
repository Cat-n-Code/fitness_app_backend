from typing import Annotated

from fastapi import APIRouter, Depends, Path

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.core.dependencies import DbSession

workouts_router = APIRouter(prefix="/workout", tags=["Шаблоны тренеровок"])


@workouts_router.get(
    "/{workout_id}",
    response_model=None,
    summary="Получение тренировки",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_workout(
    session: DbSession,
    user: AuthenticateUser,
    workout_id: Annotated[int, Path],
):
    return None


@workouts_router.get(
    "customer/{customer_id}",
    response_model=None,
    summary="Получить список тренировок клиента",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_workout_by_customer(
    session: DbSession,
    user: AuthenticateUser,
    customer_id: Annotated[int, Path],
):
    return None


@workouts_router.post(
    "customer/{customer_id}",
    response_model=None,
    summary="Назначение тренировки клиенту",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def create_workout(
    session: DbSession,
    user: AuthenticateUser,
    customer_id: Annotated[int, Path],
):
    return None


@workouts_router.get(
    "/exercises/{workout_id}",
    response_model=None,
    summary="Получение заданий в тренировке у клиента",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_workout_exercises(
    session: DbSession,
    user: AuthenticateUser,
    workout_id: Annotated[int, Path],
):
    return None
