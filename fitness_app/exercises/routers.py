from typing import Annotated

from fastapi import APIRouter, Depends, Path

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.core.dependencies import DbSession

exercises_router = APIRouter(prefix="/exercises", tags=["Упражнения"])


@exercises_router.get(
    "/",
    response_model=None,
    summary="Получение списка заданий",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_exercises(
    session: DbSession,
    user: AuthenticateUser,
):
    return None


@exercises_router.get(
    "/{exercise_id}",
    response_model=None,
    summary="Получение задания по id",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_exercise(
    session: DbSession, user: AuthenticateUser, exercise_id: Annotated[int, Path]
):
    return None


# Для тренера
@exercises_router.post(
    "/",
    response_model=None,
    summary="Создание задания",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def create_exercise(
    session: DbSession,
    user: AuthenticateUser,
):
    return None
