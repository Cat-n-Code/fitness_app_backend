from fastapi import APIRouter, Depends

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.coaches.models import Coach
from fitness_app.core.dependencies import DbSession

coaches_router = APIRouter(prefix="/coaches", tags=["Тренеры"])


@coaches_router.get(
    "/current",
    summary="Получить текущего авторизованного пользователя",
    response_model=None,
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_current_coach(user: AuthenticateUser) -> Coach:
    return None


@coaches_router.put(
    "/current",
    summary="Обновить текущего авторизованного тренера",
    response_model=None,
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def update_current_coach(
    session: DbSession,
    user: AuthenticateUser,
) -> Coach:
    return None
