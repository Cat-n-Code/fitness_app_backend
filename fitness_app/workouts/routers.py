from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Path, status

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.core.dependencies import (
    DbSession,
    ExerciseWorkoutServiceDep,
    WorkoutServiceDep,
)
from fitness_app.core.utils import PageField, SizeField
from fitness_app.workouts.schemas import (
    ExerciseWorkoutCreateSchema,
    ExerciseWorkoutSchema,
    ExerciseWorkoutUpdateSchema,
    WorkoutCreateSchema,
    WorkoutSchema,
    WorkoutUpdateSchema,
)

workouts_router = APIRouter(prefix="/workouts", tags=["Тренировки"])


@workouts_router.post(
    "",
    response_model=WorkoutSchema,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Необходимо указать свой coach_id или customer_id"
        }
    },
    summary="Создание тренировки",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def create(
    session: DbSession,
    service: WorkoutServiceDep,
    user: AuthenticateUser,
    schema: WorkoutCreateSchema,
) -> WorkoutSchema:
    return await service.create(session, user, schema)


@workouts_router.get(
    "/{id}",
    response_model=WorkoutSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Тренировки с указанным id не найдено"
        }
    },
    summary="Получение тренировки по id",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_by_id(
    session: DbSession,
    service: WorkoutServiceDep,
    id: Annotated[int, Path],
) -> WorkoutSchema:
    return await service.get_by_id(session, id)


@workouts_router.get(
    "/users/current",
    response_model=list[WorkoutSchema],
    summary="Получить список тренировок текущего пользователя",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_workouts_by_user(
    session: DbSession,
    service: WorkoutServiceDep,
    user: AuthenticateUser,
    page: PageField = 0,
    size: SizeField = 10,
    date_start: Optional[date] = None,
    date_finish: Optional[date] = None,
) -> list[WorkoutSchema]:
    return await service.get_workouts_by_user(
        session,
        user,
        page,
        size,
        date_start,
        date_finish,
    )


@workouts_router.put(
    "",
    summary="Обновить тренировку по id",
    response_model=WorkoutSchema,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Нельзя изменять не вашу тренировку"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Тренировки с указанным id не найдено"
        },
    },
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def update_by_id(
    session: DbSession,
    user: AuthenticateUser,
    service: WorkoutServiceDep,
    schema: WorkoutUpdateSchema,
) -> WorkoutSchema:
    return await service.update_by_id(
        session,
        user,
        schema,
    )


@workouts_router.delete(
    "/{id}",
    summary="Удаление задания по id",
    response_model=WorkoutSchema,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Нельзя изменять не вашу тренировку"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Упражнения с указанным id не найдено"
        },
    },
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def delete_by_id(
    session: DbSession,
    user: AuthenticateUser,
    service: WorkoutServiceDep,
    id: Annotated[int, Path],
) -> WorkoutSchema:
    return await service.delete_by_id(session, user, id)


@workouts_router.post(
    "/exercises",
    response_model=ExerciseWorkoutCreateSchema,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Необходимо указать свой coach_id или customer_id"
        },
    },
    summary="Создание упражнения для тренировки",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def create_exercise_workout(
    session: DbSession,
    service: ExerciseWorkoutServiceDep,
    user: AuthenticateUser,
    schema: ExerciseWorkoutCreateSchema,
) -> ExerciseWorkoutSchema:
    return await service.create(session, user, schema)


@workouts_router.put(
    "/exercises/{exercise_workout_id}",
    summary="Обновить упражнение для тренировки по id",
    response_model=ExerciseWorkoutSchema,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Нельзя изменять не вашу тренировку"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Упражнения для тренировки с указанным id не найдено"
        },
    },
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def update_exercise_workout_by_id(
    session: DbSession,
    user: AuthenticateUser,
    service: ExerciseWorkoutServiceDep,
    schema: ExerciseWorkoutUpdateSchema,
) -> ExerciseWorkoutSchema:
    return await service.update_by_id(
        session,
        user,
        schema,
    )


@workouts_router.delete(
    "/exercises/{exercise_workout_id}",
    summary="Удаление задания для тренировки по id",
    response_model=ExerciseWorkoutSchema,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Нельзя изменять не вашу тренировку"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Упражнения для тренировки с указанным id не найдено"
        },
    },
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def delete_exercise_workout_by_id(
    session: DbSession,
    user: AuthenticateUser,
    service: ExerciseWorkoutServiceDep,
    exercise_workout_id: Annotated[int, Path],
) -> ExerciseWorkoutSchema:
    return await service.delete_by_id(session, user, exercise_workout_id)
