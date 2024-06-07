from sqlalchemy.ext.asyncio import AsyncSession

from fitness_app.chats.models import Chat
from fitness_app.chats.repositories import ChatRepository
from fitness_app.core.exceptions import EntityNotFoundException, ForbiddenException
from fitness_app.core.schemas import PageSchema
from fitness_app.users.models import User
from fitness_app.users.schemas import UserSchema
from fitness_app.users.services import UserService


class ChatService:
    def __init__(
        self,
        chat_repository: ChatRepository,
        user_service: UserService,
    ):
        self._chat_repository = chat_repository
        self._user_service = user_service

    async def create(
        self, session: AsyncSession, users: list, for_workout: bool = False
    ):
        chat = Chat()
        setattr(chat, "users", users)
        setattr(chat, "messages", [])
        if not for_workout:
            for user in users:
                user.chats.append(chat)

        return await self._chat_repository.save(session, chat)

    async def get_chat(self, session: AsyncSession, user: User, chat_id: int):
        chat = await self._chat_repository.get_with_users(session, chat_id)
        if chat is None:
            raise EntityNotFoundException("Chat with given id was not found")
        if user not in chat.users:
            raise ForbiddenException("Authenticated user is not a member of this chat")

        return chat

    async def is_accessed_chat(self, session: AsyncSession, user: User, chat_id: int):
        chat = await self._chat_repository.get_with_users(session, chat_id)
        if chat is None:
            raise EntityNotFoundException("Chat with given id was not found")
        if user not in chat.users:
            raise ForbiddenException("Authenticated user is not a member of this chat")

        return True

    async def get_chats_by_user(
        self,
        session: AsyncSession,
        user: User,
        page: int,
        size: int,
    ):
        total_chats_count = await self._chat_repository.count_chats(session, user.id)
        chats = await self._chat_repository.get_chats(session, user.id, page, size)
        chat_dicts = [chat.__dict__ for chat in chats]
        print("dicts:\\n", chat_dicts)
        for chat_dict in chat_dicts:
            chat_dict["users"] = [
                UserSchema.model_validate(user) for user in chat_dict["users"]
            ]
        return PageSchema(total_items_count=total_chats_count, items=chat_dicts)
