from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fitness_app.coaches.models import Coach
from fitness_app.customers.models import Customer


class CoachRepository:

    async def save(self, session: AsyncSession, coach: Coach):
        session.add(coach)
        await session.flush()
        await session.commit()
        return coach

    async def delete(self, session: AsyncSession, coach: Coach):
        await session.delete(coach)
        await session.commit()
        return coach

    async def get_all(
        self,
        session: AsyncSession,
        page: int,
        size: int,
    ):
        statement = select(Coach).order_by(Coach.id)
        statement.offset(page * size).limit(size)
        result = await session.execute(statement)
        return result.scalars().all()

    async def get_coaches_by_id(
        self,
        session: AsyncSession,
        coach_id: int,
        page: int,
        size: int,
    ):
        statement = (
            select(Coach)
            .where(Coach.id == coach_id)
            .options(selectinload(Coach.customers))
        )
        statement.offset(page * size).limit(size)
        result = await session.execute(statement)
        return result.scalar_one().customers

    async def count_coaches_by_user_id(self, session: AsyncSession, coach_id: int):
        statement = (
            select(func.count(Customer.id))
            .join(Coach.customers)
            .where(Coach.id == coach_id)
        )

        result = await session.execute(statement)
        return result.scalar_one()

    async def count_all(
        self,
        session: AsyncSession,
    ):
        statement = select(func.count()).select_from(Coach)
        result = await session.execute(statement)
        return result.scalar_one()
