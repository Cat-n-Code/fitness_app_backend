from typing import Optional

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from fitness_app.core.exceptions import EntityNotFoundException, ForbiddenException
from fitness_app.core.utils import update_model_by_schema
from fitness_app.exercises.models import Exercise
from fitness_app.exercises.repositories import ExerciseRepository
from fitness_app.exercises.schemas import (
    ExerciseCreateSchema,
    ExerciseFindSchema,
    ExerciseUpdateSchema,
)
from fitness_app.file_entities.services import FileEntityService
from fitness_app.users.models import User


class ExerciseService:
    def __init__(
        self,
        exercise_repository: ExerciseRepository,
        file_entity_service: FileEntityService,
    ):
        self._exercise_repository = exercise_repository
        self._file_entity_service = file_entity_service

    async def create(
        self,
        session: AsyncSession,
        schema: ExerciseCreateSchema,
        photos: Optional[list[UploadFile]],
        user: User,
    ):
        exercise = Exercise(**schema.model_dump())
        exercise.user_id = user.id
        exercise = await self._exercise_repository.save(session, exercise)

        if photos:
            for photo in photos:
                await self._file_entity_service.create(session, photo, exercise.id)

        return await self._exercise_repository.get_by_id(session, exercise.id)

    async def get_by_id(self, session: AsyncSession, id: int):
        exercise = await self._exercise_repository.get_by_id(session, id)
        if not exercise:
            raise EntityNotFoundException("Упражнения с указанным id не найдено")
        return exercise

    async def get_by_user_id(
        self,
        session: AsyncSession,
        user_id: int,
        find_schema: Optional[ExerciseFindSchema],
        page: int,
        size: int,
    ):
        return await self._exercise_repository.get_by_user_id(
            session, user_id, find_schema, page, size
        )

    async def update_by_id(
        self,
        session: AsyncSession,
        user_id: int,
        schema: ExerciseUpdateSchema,
        photos: list[UploadFile],
    ):
        exercise = await self._exercise_repository.get_by_id(session, schema.id)
        if not exercise:
            raise EntityNotFoundException("Упражнения с указанным id не найдено")
        if not exercise.user_id:
            raise ForbiddenException("Отказано в доступе")
        if exercise.user_id != user_id:
            raise ForbiddenException("Можно изменять только свои упражнения")

        update_model_by_schema(exercise, schema)
        exercise = await self._exercise_repository.save(session, exercise)

        if exercise.photos:
            for photo in exercise.photos:
                await self._file_entity_service.delete_by_id(session, photo.id)
        if photos:
            for photo in photos:
                await self._file_entity_service.create(session, photo, exercise.id)

        await session.refresh(exercise)
        return exercise

    async def delete_by_id(self, session: AsyncSession, user_id: int, id: int):
        exercise = await self._exercise_repository.get_by_id(session, id)
        if not exercise:
            raise EntityNotFoundException("Упражнения с указанным id не найдено")
        if not exercise.user_id:
            raise ForbiddenException("Отказано в доступе")
        if exercise.user_id != user_id:
            raise ForbiddenException("Можно изменять только свои упражнения")

        if exercise.photos:
            for i in range(len(exercise.photos)):
                await self._file_entity_service.delete_by_id(
                    session, exercise.photos[i].id
                )

        return await self._exercise_repository.delete(session, exercise)
