from sqlalchemy.ext.asyncio import AsyncSession

from fitness_app.coaches.models import Coach


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
