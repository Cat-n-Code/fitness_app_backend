from sqlalchemy.ext.asyncio import AsyncSession

from fitness_app.chats.models import Chat
from fitness_app.chats.services import ChatService
from fitness_app.core.schemas import PageSchema
from fitness_app.messages.models import Message
from fitness_app.messages.repositories import MessageRepository
from fitness_app.messages.schemas import MessageBaseSchema, MessageCreateSchema
from fitness_app.users.models import User


class MessageService:
    def __init__(
        self,
        message_repository: MessageRepository,
        chat_service: ChatService,
    ):
        self._message_repository = message_repository
        self._chat_service = chat_service

    async def get_messages_by_chat_id(
        self,
        session: AsyncSession,
        user: User,
        chat_id: int,
        page: int,
        size: int,
    ):
        await self._chat_service.is_accessed_chat(session, user, chat_id)
        total_messages_count = await self._message_repository.count_messages(
            session, chat_id
        )
        messages = await self._message_repository.get_messagees(
            session, chat_id, page, size
        )
        return PageSchema(total_items_count=total_messages_count, items=messages)

    async def create(
        self,
        session: AsyncSession,
        user: User,
        create_schema: MessageCreateSchema,
    ):
        await self._chat_service.is_accessed_chat(session, user, create_schema.chat_id)
        chat = await session.get(Chat, create_schema.chat_id)
        create_schema_dict = create_schema.model_dump()
        create_schema_dict["sender_id"] = user.id
        messageSchema = MessageBaseSchema(**create_schema_dict)
        message = Message(**messageSchema.model_dump())
        saved_message = await self._message_repository.save(session, message)
        chat.last_timestamp = saved_message.timestamp
        await session.commit()
        return saved_message
