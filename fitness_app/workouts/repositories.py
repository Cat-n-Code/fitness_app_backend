from datetime import date
from typing import Optional

from sqlalchemy import and_, desc, null, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from fitness_app.chats.models import Chat
from fitness_app.exercises.models import Exercise
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
                joinedload(Workout.chat).options(selectinload(Chat.users)),
                selectinload(Workout.exercise_workouts).options(
                    joinedload(ExerciseWorkout.exercise).options(
                        selectinload(Exercise.photos)
                    ),
                    joinedload(ExerciseWorkout.workout),
                ),
            )
        )

        result = await session.execute(statement)
        workout = result.scalar_one_or_none()
        if workout and workout.exercise_workouts:
            workout.exercise_workouts.sort(key=lambda workout: workout.num_order)
        return workout

    async def get_workouts_by_coach_id(
        self,
        session: AsyncSession,
        coach_id: int,
        page: int,
        size: int,
        date_start: Optional[date] = None,
        date_finish: Optional[date] = None,
    ):
        statement = select(Workout).where(
            or_(
                Workout.coach_id == coach_id,
                and_(Workout.coach_id == null(), Workout.customer_id == null()),
            )
        )
        if date_start:
            statement = statement.where(Workout.date_field >= date_start)
        if date_finish:
            statement = statement.where(Workout.date_field <= date_finish)
        statement = (
            statement.offset(page * size)
            .limit(size)
            .order_by(desc(Workout.date_field))
            .options(
                joinedload(Workout.customer),
                joinedload(Workout.coach),
                joinedload(Workout.chat).options(selectinload(Chat.users)),
                selectinload(Workout.exercise_workouts).options(
                    joinedload(ExerciseWorkout.exercise).options(
                        selectinload(Exercise.photos)
                    ),
                    joinedload(ExerciseWorkout.workout),
                ),
            )
        )

        result = await session.execute(statement)
        workouts = result.scalars().all()
        for workout in workouts:
            if workout.exercise_workouts:
                workout.exercise_workouts.sort(key=lambda workout: workout.num_order)
        return workouts

    async def get_workouts_by_customer_id(
        self,
        session: AsyncSession,
        customer_id: int,
        page: int,
        size: int,
        date_start: Optional[date] = None,
        date_finish: Optional[date] = None,
    ):
        statement = select(Workout).where(
            or_(
                Workout.customer_id == customer_id,
                and_(Workout.coach_id == null(), Workout.customer_id == null()),
            )
        )
        if date_start:
            statement = statement.where(Workout.date_field >= date_start)
        if date_finish:
            statement = statement.where(Workout.date_field <= date_finish)
        statement = (
            statement.offset(page * size)
            .limit(size)
            .order_by(desc(Workout.date_field))
            .options(
                joinedload(Workout.customer),
                joinedload(Workout.coach),
                joinedload(Workout.chat).options(selectinload(Chat.users)),
                selectinload(Workout.exercise_workouts).options(
                    joinedload(ExerciseWorkout.exercise).options(
                        selectinload(Exercise.photos)
                    ),
                    joinedload(ExerciseWorkout.workout),
                ),
            )
        )

        result = await session.execute(statement)
        workouts = result.scalars().all()
        for workout in workouts:
            if workout.exercise_workouts:
                workout.exercise_workouts.sort(key=lambda workout: workout.num_order)
        return workouts

    async def update(self, session: AsyncSession, workout: Workout):
        session.add(workout)
        await session.flush()
        await session.commit()
        await session.refresh(workout)
        return workout

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
            .options(
                joinedload(ExerciseWorkout.exercise).options(
                    selectinload(Exercise.photos)
                ),
                joinedload(ExerciseWorkout.workout),
            )
        )
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def update(self, session: AsyncSession, exercise_workout: ExerciseWorkout):
        session.add(exercise_workout)
        await session.flush()
        await session.commit()
        await session.refresh(exercise_workout)
        return exercise_workout

    async def delete(self, session: AsyncSession, exercise_workout: ExerciseWorkout):
        await session.delete(exercise_workout)
        await session.commit()
        return exercise_workout
