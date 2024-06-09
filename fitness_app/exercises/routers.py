from typing import Annotated

from fastapi import APIRouter, Depends, Path, UploadFile, status
from pydantic import Json

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.core.dependencies import DbSession, ExerciseServiceDep
from fitness_app.core.utils import PageField, SizeField
from fitness_app.exercises.schemas import (
    ExerciseCreateSchema,
    ExerciseSchema,
    ExerciseUpdateSchema,
)

exercises_router = APIRouter(prefix="/exercises", tags=["Упражнения"])


@exercises_router.post(
    "",
    response_model=ExerciseSchema,
    summary="Создание задания",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def create(
    session: DbSession,
    service: ExerciseServiceDep,
    user: AuthenticateUser,
    schema: Json[ExerciseCreateSchema],
    photos: list[UploadFile],
) -> ExerciseSchema:
    return await service.create(
        session,
        schema,
        photos,
        user,
    )


@exercises_router.get(
    "/{id}",
    response_model=ExerciseSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Упражнения с указанным id не найдено"
        }
    },
    summary="Получение задания по id",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_by_id(
    session: DbSession, service: ExerciseServiceDep, id: Annotated[int, Path]
) -> ExerciseSchema:
    return await service.get_by_id(session, id)


@exercises_router.get(
    "/users/current",
    response_model=list[ExerciseSchema],
    summary="Получение заданий текущего пользователя",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_by_user_id(
    session: DbSession,
    service: ExerciseServiceDep,
    user: AuthenticateUser,
    page: PageField = 0,
    size: SizeField = 10,
) -> list[ExerciseSchema]:
    return await service.get_by_user_id(session, user.id, page, size)


@exercises_router.put(
    "",
    summary="Обновить задание",
    response_model=ExerciseSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Упражнения с указанным id не найдено"
        }
    },
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def update_by_id(
    session: DbSession,
    service: ExerciseServiceDep,
    schema: Json[ExerciseUpdateSchema],
    photos: list[UploadFile],
) -> ExerciseSchema:
    return await service.update_by_id(session, schema, photos)


@exercises_router.delete(
    "/{id}",
    summary="Удаление задания по id",
    response_model=ExerciseSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Упражнения с указанным id не найдено"
        }
    },
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def delete_by_id(
    session: DbSession, service: ExerciseServiceDep, id: Annotated[int, Path]
) -> ExerciseSchema:
    return await service.delete_by_id(session, id)


# //////////////////////////////////////////////////////////////////////////..............................//////////////
# Удалять и обновлять только владелец/////////////////////////////////////////////////////////////////////////////////////
