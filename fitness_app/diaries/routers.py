from datetime import date

from fastapi import APIRouter, Depends, status

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.core.dependencies import DbSession, DiaryServiceDep
from fitness_app.diaries.schemas import DiaryCreateSchema, DiarySchema

diaries_router = APIRouter(prefix="/diaries", tags=["Дневники"])


@diaries_router.get(
    "",
    summary="Получить дневники за определенный период",
    response_model=list[DiarySchema],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Дневники за данный период не были найдены"
        },
    },
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_diaries_by_dates(
    session: DbSession,
    service: DiaryServiceDep,
    user: AuthenticateUser,
    date_start: date,
    date_finish: date,
) -> list[DiarySchema]:
    return await service.get_by_dates(session, user.id, date_start, date_finish)


@diaries_router.put(
    "",
    summary="Создать сегодняшний дневник",
    response_model=DiarySchema,
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def create_or_update_today_diary(
    session: DbSession,
    service: DiaryServiceDep,
    user: AuthenticateUser,
    schema: DiaryCreateSchema,
) -> DiarySchema:
    return await service.create_or_update(session, user.id, schema)
