from typing import Annotated

from fastapi import APIRouter, Depends, Path

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.core.dependencies import DbSession

workout_templates_router = APIRouter(
    prefix="/workout_templates", tags=["Шаблоны тренеровок"]
)


# Для тренера
@workout_templates_router.get(
    "/",
    response_model=None,
    summary="Получение списка своих шаблонов тренировок",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_own_templates(
    session: DbSession,
    user: AuthenticateUser,
):
    return None


# Для тренера
@workout_templates_router.get(
    "/{template_id}",
    response_model=None,
    summary="Получение списка своих шаблонов тренировок",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_own_template(
    session: DbSession, user: AuthenticateUser, template_id: Annotated[int, Path]
):
    return None


# Для тренера
@workout_templates_router.post(
    "/",
    response_model=None,
    summary="Создание своего шаблона тренировки",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def create_own_templates(
    session: DbSession,
    user: AuthenticateUser,
):
    return None
