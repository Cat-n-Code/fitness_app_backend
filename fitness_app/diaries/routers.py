from datetime import date
from typing import List

from fastapi import APIRouter, Depends, status

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.core.dependencies import DbSession, DiaryServiceDep
from fitness_app.diaries.schemas import DiaryCreateSchema, DiarySchema

diaries_router = APIRouter(prefix="/diaries", tags=["Diaries"])


@diaries_router.get(
    "",
    summary="Get diaries for a specific period",
    response_model=List[DiarySchema],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The diaries with given dates was not found"
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
):
    diaries = await service.get_by_dates(session, user.id, date_start, date_finish)
    validated_diaries = [DiarySchema.model_validate(diary) for diary in diaries]
    return validated_diaries


@diaries_router.put(
    "",
    summary="Create today diary",
    response_model=DiarySchema,
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def create_or_update_today_diary(
    session: DbSession,
    service: DiaryServiceDep,
    user: AuthenticateUser,
    schema: DiaryCreateSchema,
):
    diary = await service.create_or_update(session, user.id, schema)
    return DiarySchema.model_validate(diary)
