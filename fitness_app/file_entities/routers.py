from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import FileResponse

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
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
    summary="Получение файла по filename",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_by_filename(
    session: DbSession,
    service: FileEntityServiceDep,
    background_tasks: BackgroundTasks,
    user: AuthenticateUser,
    filename: str,
) -> FileResponse:
    return await service.get_by_filename(session, background_tasks, filename, user.id)
