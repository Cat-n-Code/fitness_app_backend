from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from fitness_app.core.exceptions import EntityNotFoundException
from fitness_app.core.utils import update_model_by_schema
from fitness_app.diaries.models import DiaryEntry
from fitness_app.diaries.repositories import DiaryRepository
from fitness_app.diaries.schemas import DiaryCreateSchema


class DiaryService:
    def __init__(self, diary_repository: DiaryRepository):
        self._diary_repository = diary_repository

    async def get_by_dates(
        self, session: AsyncSession, user_id: int, date_start: date, date_finish: date
    ):
        diaries = await self._diary_repository.get_by_dates(
            session, user_id, date_start, date_finish
        )
        if diaries == []:
            raise EntityNotFoundException("The diaries with given dates was not found")

        return diaries

    async def create_or_update(
        self, session: AsyncSession, user_id: int, schema: DiaryCreateSchema
    ):
        date_field = date.today()
        if await self._diary_repository.exists_by_user_id_and_date(
            session, user_id, date_field
        ):
            diary = await self._diary_repository.get_by_user_id_and_date(
                session, user_id, date_field
            )
            update_model_by_schema(diary, schema)
        else:
            diary = DiaryEntry(
                **schema.model_dump(), user_id=user_id, date_field=date_field
            )

        return await self._diary_repository.save(session, diary)
