from fastapi import APIRouter, Depends

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.chats.schemas import ChatSchema
from fitness_app.core.dependencies import ChatServiceDep, DbSession
from fitness_app.core.schemas import PageSchema
from fitness_app.core.utils import IdField, PageField, SizeField

chats_router = APIRouter(prefix="/chats", tags=["Чаты"])


@chats_router.get(
    "/mine",
    summary="Получить список своих чатов (вне тренеровок)",
    response_model=PageSchema,
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_all(
    session: DbSession,
    service: ChatServiceDep,
    user: AuthenticateUser,
    page: PageField = 0,
    size: SizeField = 10,
):
    chats = await service.get_chats_by_user(session, user, page, size)
    return PageSchema(
        total_items_count=chats.total_items_count,
        items=list(map(ChatSchema.model_validate, chats.items)),
    )


@chats_router.get(
    "/get/{chat_id}",
    response_model=ChatSchema,
    summary="Получение чата по id",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_chat(
    session: DbSession,
    service: ChatServiceDep,
    user: AuthenticateUser,
    chat_id: IdField,
):
    chat = await service.get_chat(session, user, chat_id)
    return ChatSchema.model_validate(chat)
