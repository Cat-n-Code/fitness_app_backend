from typing import Annotated

from fastapi import APIRouter, Depends, Path

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.core.dependencies import DbSession

chats_router = APIRouter(prefix="/chats", tags=["Тренеры"])


@chats_router.get(
    "/{chat_id}",
    response_model=None,
    summary="Получение чата по id",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_chat(
    session: DbSession,
    user: AuthenticateUser,
    chat_id: Annotated[int, Path],
):
    return None


@chats_router.get(
    "/customer/{customer_id}",
    response_model=None,
    summary="Получение чата с клиентом",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_chat_by_coach(
    session: DbSession,
    user: AuthenticateUser,
    customer_id: Annotated[int, Path],
):
    return None


@chats_router.get(
    "/coaches/my",
    response_model=None,
    summary="Получение чата с тренером",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_chat_by_customer(
    session: DbSession,
    user: AuthenticateUser,
):
    return None
