from datetime import date

from fastapi import APIRouter, Depends, status

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.core.dependencies import DbSession, WaterEntryServiceDep
from fitness_app.water_entries.schemas import WaterEntryCreateSchema, WaterEntrySchema

water_entries_router = APIRouter(prefix="/waters", tags=["Waters"])


@water_entries_router.get(
    "",
    summary="Get water volume for a specific period",
    response_model=list[WaterEntrySchema],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The water entity with given dates was not found"
        },
    },
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_water_entries_by_dates(
    session: DbSession,
    service: WaterEntryServiceDep,
    user: AuthenticateUser,
    date_start: date,
    date_finish: date,
) -> list[WaterEntrySchema]:
    return await service.get_by_dates(session, user.id, date_start, date_finish)


@water_entries_router.put(
    "",
    summary="Create today water entity",
    response_model=WaterEntrySchema,
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def create_or_update(
    session: DbSession,
    service: WaterEntryServiceDep,
    user: AuthenticateUser,
    schema: WaterEntryCreateSchema,
) -> WaterEntrySchema:
    return await service.create_or_update(session, user.id, schema)
