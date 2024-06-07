import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from fitness_app.core.db_manager import DatabaseManager  # isort: split

from fitness_app.auth.routers import auth_router
from fitness_app.auth.services import AuthService, PasswordService, TokenService
from fitness_app.chats.repositories import ChatRepository
from fitness_app.chats.routers import chats_router
from fitness_app.chats.services import ChatService
from fitness_app.coaches.repositories import CoachRepository
from fitness_app.coaches.routers import coaches_router
from fitness_app.coaches.services import CoachService
from fitness_app.core.exceptions import (
    AppException,
    handle_app_exception,
    handle_validation_exception,
)
from fitness_app.core.settings import AppSettings
from fitness_app.customers.repositories import CustomerRepository
from fitness_app.customers.routers import customers_router
from fitness_app.customers.services import CustomerService
from fitness_app.exercises.repositories import ExerciseRepository
from fitness_app.exercises.routers import exercises_router
from fitness_app.exercises.services import ExerciseService
from fitness_app.file_entities.repositories import FileEntityRepository
from fitness_app.file_entities.routers import file_entities_router
from fitness_app.file_entities.services import FileEntityService
from fitness_app.messages.repositories import MessageRepository
from fitness_app.messages.routers import messages_router
from fitness_app.messages.services import MessageService
from fitness_app.users.repositories import UserRepository
from fitness_app.users.routers import users_router
from fitness_app.users.services import UserService
from fitness_app.workout_templates.routers import workout_templates_router
from fitness_app.workouts.routers import workouts_router


def create_app(settings: AppSettings | None = None) -> FastAPI:
    if settings is None:
        settings = AppSettings()

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    app = FastAPI(
        title="Приложение-ассистент для формирования плана фитнес-тренировок",
        lifespan=_app_lifespan,
        servers=[
            {"url": "http://localhost:8080", "description": "Локальный сервер"},
        ],
        responses={
            400: {"description": "Неверный формат входных данных"},
        },
    )

    """ Setup global dependencies """
    _setup_app_dependencies(app, settings)

    """ Setup middlewares """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    """ Setup routers """
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(exercises_router)
    app.include_router(file_entities_router)
    app.include_router(customers_router)
    app.include_router(coaches_router)
    app.include_router(chats_router)
    app.include_router(messages_router)
    app.include_router(exercises_router)
    app.include_router(workouts_router)
    app.include_router(workout_templates_router)

    """ Setup exception handlers """
    app.add_exception_handler(AppException, handle_app_exception)
    app.add_exception_handler(RequestValidationError, handle_validation_exception)

    return app


def _setup_app_dependencies(app: FastAPI, settings: AppSettings):
    app.state.settings = settings
    app.state.database_manager = DatabaseManager(settings.db_url)

    user_repository = UserRepository()
    file_entity_repository = FileEntityRepository()
    exercise_repository = ExerciseRepository()
    coach_repository = CoachRepository()
    customer_repository = CustomerRepository()
    message_repository = MessageRepository()
    chat_repository = ChatRepository()

    password_service = PasswordService()
    token_service = TokenService(
        settings.auth_token_secret_key, settings.auth_token_lifetime
    )
    auth_service = AuthService(password_service, token_service, user_repository)
    user_service = UserService(password_service, user_repository)
    file_entity_service = FileEntityService(
        settings.region,
        settings.aws_access_key_id,
        settings.aws_secret_access_key,
        settings.bucket_name,
        settings.aws_endpoint,
        settings.aws_access_domain_name,
        file_entity_repository,
    )
    coach_service = CoachService(coach_repository, user_repository, user_service)
    customer_service = CustomerService(
        customer_repository, user_repository, user_service
    )
    exercise_service = ExerciseService(exercise_repository, file_entity_service)
    chat_service = ChatService(chat_repository, user_service)
    message_service = MessageService(message_repository, chat_service)

    app.state.auth_service = auth_service
    app.state.user_service = user_service
    app.state.file_entity_service = file_entity_service
    app.state.exercise_service = exercise_service
    app.state.coach_service = coach_service
    app.state.customer_service = customer_service
    app.state.chat_service = chat_service
    app.state.message_service = message_service


@asynccontextmanager
async def _app_lifespan(app: FastAPI):
    # settings: AppSettings = app.state.settings
    db: DatabaseManager = app.state.database_manager

    await db.initialize()

    # if settings.initial_user is not None:
    #     user_service: UserService = app.state.user_service
    #     async with db.create_session() as session:
    #         try:
    #             await user_service.create(session, settings.initial_user)
    #             logging.info("Initial user was successfully created")
    #         except EntityAlreadyExistsException:
    #             logging.info("Initial user already exists. Skipped")

    yield
    await db.dispose()
