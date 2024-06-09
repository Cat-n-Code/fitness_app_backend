from datetime import date
from typing import Optional

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from fitness_app.workouts.models import ExerciseWorkout, Workout


class WorkoutRepository:
    async def save(self, session: AsyncSession, workout: Workout):
        session.add(workout)
        await session.flush()
        await session.commit()
        return workout

    async def get_by_id(self, session: AsyncSession, id: int):
        statement = (
            select(Workout)
            .where(Workout.id == id)
            .options(
                joinedload(Workout.customer),
                joinedload(Workout.coach),
                selectinload(Workout.exercise_workouts).options(
                    joinedload(ExerciseWorkout.exercise)
                ),
            )
        )

        exercise_workouts_exist = await session.execute(
            select(ExerciseWorkout).where(ExerciseWorkout.workout_id == id)
        )
        if exercise_workouts_exist.scalars().first() is not None:
            statement = statement.order_by(ExerciseWorkout.num_order)

        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def get_workouts_by_coach_id(
        self,
        session: AsyncSession,
        coach_id: int,
        page: int,
        size: int,
        date_start: Optional[date] = None,
        date_finish: Optional[date] = None,
    ):
        statement = select(Workout).where(Workout.coach_id == coach_id)
        if date_start:
            statement = statement.where(Workout.date_field >= date_start)
        if date_finish:
            statement = statement.where(Workout.date_field <= date_finish)
        statement = (
            statement.order_by(desc(Workout.date_field))
            .offset(page * size)
            .limit(size)
            .options(
                joinedload(Workout.customer),
                joinedload(Workout.coach),
                selectinload(Workout.exercise_workouts).options(
                    joinedload(ExerciseWorkout.exercise)
                ),
            )
            .order_by(ExerciseWorkout.num_order)
        )

        result = await session.execute(statement)
        return result.scalars().all()

    async def get_workouts_by_customer_id(
        self,
        session: AsyncSession,
        customer_id: int,
        page: int,
        size: int,
        date_start: Optional[date] = None,
        date_finish: Optional[date] = None,
    ):
        statement = select(Workout).where(Workout.customer_id == customer_id)
        if date_start:
            statement = statement.where(Workout.date_field >= date_start)
        if date_finish:
            statement = statement.where(Workout.date_field <= date_finish)
        statement = (
            statement.order_by(desc(Workout.date_field))
            .offset(page * size)
            .limit(size)
            .options(
                joinedload(Workout.customer),
                joinedload(Workout.coach),
                selectinload(Workout.exercise_workouts).order_by(
                    ExerciseWorkout.num_order
                ),
            )
        )

        result = await session.execute(statement)
        return result.scalars().all()

    async def delete(self, session: AsyncSession, workout: Workout):
        await session.delete(workout)
        await session.commit()
        return workout


class ExerciseWorkoutRepository:
    async def save(self, session: AsyncSession, exercise_workout: ExerciseWorkout):
        session.add(exercise_workout)
        await session.flush()
        await session.commit()
        return exercise_workout

    async def get_by_id(self, session: AsyncSession, id: int):
        statement = (
            select(ExerciseWorkout)
            .where(ExerciseWorkout.id == id)
            .options(joinedload(ExerciseWorkout.workout))
        )
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def delete(self, session: AsyncSession, exercise_workout: ExerciseWorkout):
        await session.delete(exercise_workout)
        await session.commit()
        return exercise_workout
