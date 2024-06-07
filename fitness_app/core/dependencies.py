from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from fitness_app.auth.services import AuthService
from fitness_app.core.db_manager import DatabaseManager
from fitness_app.exercises.services import ExerciseService
from fitness_app.file_entities.services import FileEntityService
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


DbSession = Annotated[AsyncSession, Depends(db_session)]
AuthServiceDep = Annotated[AuthService, Depends(auth_service)]
UserServiceDep = Annotated[UserService, Depends(user_service)]
FileEntityServiceDep = Annotated[FileEntityService, Depends(file_entity_service)]
ExerciseServiceDep = Annotated[ExerciseService, Depends(exercise_service)]
