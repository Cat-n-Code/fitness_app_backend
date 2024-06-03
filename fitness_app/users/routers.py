from fastapi import APIRouter, Depends, status

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Anonymous, Authenticated
from fitness_app.core.dependencies import DbSession, UserServiceDep
from fitness_app.users.schemas import (
    UserCreateSchema,
    UserPasswordUpdateSchema,
    UserSchema,
    UserUpdateSchema,
)

users_router = APIRouter(prefix="/users", tags=["Пользователи"])


@users_router.post(
    "/registration",
    summary="Регистрация нового пользователя",
    response_model=UserSchema,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Другой пользователь с указанным `email` уже существует"
        }
    },
    dependencies=[Depends(HasPermission(Anonymous()))],
)
async def register_user(
    session: DbSession, service: UserServiceDep, schema: UserCreateSchema
):
    user = await service.create(session, schema)
    return UserSchema.model_validate(user)


@users_router.get(
    "/current",
    summary="Получить текущего авторизованного пользователя",
    response_model=UserSchema,
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_current_user(user: AuthenticateUser):
    return UserSchema.model_validate(user)


@users_router.put(
    "/current",
    summary="Обновить текущего авторизованного пользователя",
    response_model=UserSchema,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Другой пользователь с указанным `email` уже существует"
        }
    },
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def update_current_user(
    session: DbSession,
    user_service: UserServiceDep,
    user: AuthenticateUser,
    schema: UserUpdateSchema,
):
    new_user = await user_service.update_by_id(session, user.id, schema)
    return UserSchema.model_validate(new_user)


@users_router.put(
    "/current/password",
    summary="Обновить пароль текущего авторизованного пользователя",
    response_model=UserSchema,
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def update_current_user_password(
    session: DbSession,
    user_service: UserServiceDep,
    user: AuthenticateUser,
    schema: UserPasswordUpdateSchema,
):
    user = await user_service.update_password_by_id(session, user.id, schema.password)
    return UserSchema.model_validate(user)
