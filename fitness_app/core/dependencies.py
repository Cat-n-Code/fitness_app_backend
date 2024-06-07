from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from fitness_app.auth.services import AuthService
from fitness_app.chats.services import ChatService
from fitness_app.coaches.services import CoachService
from fitness_app.core.db_manager import DatabaseManager
from fitness_app.customers.services import CustomerService
from fitness_app.exercises.services import ExerciseService
from fitness_app.file_entities.services import FileEntityService
from fitness_app.messages.services import MessageService
from fitness_app.users.services import UserService


def db_manager(request: Request) -> DatabaseManager:
    return request.app.state.database_manager


async def db_session(db_manager: Annotated[DatabaseManager, Depends(db_manager)]):
    async with db_manager.create_session() as session:
        yield session


def auth_service(request: Request) -> AuthService:
    return request.app.state.auth_service


def user_service(request: Request) -> UserService:
    return request.app.state.user_service


def file_entity_service(request: Request) -> FileEntityService:
    return request.app.state.file_entity_service


def exercise_service(request: Request) -> ExerciseService:
    return request.app.state.exercise_service


def coach_service(request: Request) -> CoachService:
    return request.app.state.coach_service


def customer_service(request: Request) -> CustomerService:
    return request.app.state.customer_service


def message_service(request: Request) -> MessageService:
    return request.app.state.message_service


def chat_service(request: Request) -> ChatService:
    return request.app.state.chat_service


DbSession = Annotated[AsyncSession, Depends(db_session)]
AuthServiceDep = Annotated[AuthService, Depends(auth_service)]
UserServiceDep = Annotated[UserService, Depends(user_service)]
FileEntityServiceDep = Annotated[FileEntityService, Depends(file_entity_service)]
ExerciseServiceDep = Annotated[ExerciseService, Depends(exercise_service)]
CoachServiceDep = Annotated[CoachService, Depends(coach_service)]
CustomerServiceDep = Annotated[CustomerService, Depends(customer_service)]
MessageServiceDep = Annotated[MessageService, Depends(message_service)]
ChatServiceDep = Annotated[ChatService, Depends(chat_service)]
