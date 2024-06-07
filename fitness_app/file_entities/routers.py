from fastapi import APIRouter, Depends, status

from fitness_app.auth.dependencies import HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.core.dependencies import DbSession, FileEntityServiceDep

file_entities_router = APIRouter(prefix="/files", tags=["Файлы"])


@file_entities_router.get(
    "/{filename:path}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Файла с указанным filename не найдено"
        }
    },
    response_model=str,
    summary="Получение ссылки на файл по filename",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_by_filename(
    session: DbSession,
    service: FileEntityServiceDep,
    filename: str,
) -> str:
    return await service.get_by_filename(session, filename)
