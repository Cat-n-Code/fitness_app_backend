from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Path, Query, status

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.core.dependencies import DbSession, ExerciseServiceDep
from fitness_app.core.utils import PageField, SizeField
from fitness_app.exercises.schemas import (
    Difficulty,
    ExerciseCreateSchema,
    ExerciseFindSchema,
    ExerciseSchema,
    ExerciseType,
    ExerciseUpdateSchema,
)


def get_exercise_find_schema(
    name: Optional[str] = Query(None),
    muscle: Optional[str] = Query(None),
    additionalMuscle: Optional[str] = Query(None),
    type: Optional[ExerciseType] = Query(None),
    equipment: Optional[str] = Query(None),
    difficulty: Optional[Difficulty] = Query(None),
    description: Optional[str] = Query(None),
) -> ExerciseFindSchema:
    return ExerciseFindSchema(
        name=name,
        muscle=muscle,
        additionalMuscle=additionalMuscle,
        type=type,
        equipment=equipment,
        difficulty=difficulty,
        description=description,
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
    schema: ExerciseCreateSchema,
) -> ExerciseSchema:
    return await service.create(
        session,
        schema,
        user.id,
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
    summary="Получение заданий пользователя по user_id",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_by_user_id(
    session: DbSession,
    service: ExerciseServiceDep,
    user: AuthenticateUser,
    find_schema: Optional[ExerciseFindSchema] = Depends(get_exercise_find_schema),
    page: PageField = 0,
    size: SizeField = 10,
) -> list[ExerciseSchema]:
    return await service.get_by_user_id(session, user.id, find_schema, page, size)


@exercises_router.put(
    "",
    summary="Обновить задание",
    response_model=ExerciseSchema,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Можно изменять только свои упражнения"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Упражнения с указанным id не найдено"
        },
    },
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def update_by_id(
    session: DbSession,
    service: ExerciseServiceDep,
    user: AuthenticateUser,
    schema: ExerciseUpdateSchema,
) -> ExerciseSchema:
    return await service.update_by_id(session, user.id, schema)


@exercises_router.delete(
    "/{id}",
    summary="Удаление задания по id",
    response_model=ExerciseSchema,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Можно изменять только свои упражнения"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Упражнения с указанным id не найдено"
        },
    },
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def delete_by_id(
    session: DbSession,
    service: ExerciseServiceDep,
    user: AuthenticateUser,
    id: Annotated[int, Path],
) -> ExerciseSchema:
    return await service.delete_by_id(session, user.id, id)
