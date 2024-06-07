from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fitness_app.exercises.models import Exercise, UserExercises


class ExerciseRepository:
    async def save(self, session: AsyncSession, exercise: Exercise):
        session.add(exercise)
        await session.flush()
        await session.commit()
        return exercise

    async def get_by_id(self, session: AsyncSession, id: int):
        statement = (
            select(Exercise)
            .where(Exercise.id == id)
            .options(selectinload(Exercise.photos))
        )
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_user_id(
        self, session: AsyncSession, user_id: int, page: int, size: int
    ):
        statement = (
            select(Exercise)
            .join(UserExercises, Exercise.id == UserExercises.exercise_id)
            .filter(UserExercises.user_id == user_id)
            .offset(page * size)
            .limit(size)
            .options(selectinload(Exercise.photos))
        )
        result = await session.execute(statement)
        return result.scalars().all()

    async def delete(self, session: AsyncSession, exercise: Exercise):
        await session.delete(exercise)
        await session.commit()
        return exercise
