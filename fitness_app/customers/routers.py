from typing import Annotated

from fastapi import APIRouter, Depends, Path

from fitness_app.auth.dependencies import AuthenticateUser, HasPermission
from fitness_app.auth.permissions import Authenticated
from fitness_app.coaches.models import Coach
from fitness_app.core.dependencies import DbSession
from fitness_app.customers.models import Customer

customers_router = APIRouter(prefix="/coaches", tags=["Клиенты"])


@customers_router.get(
    "/current",
    response_model=None,
    summary="Получить текущего авторизованного клиента",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_current_customer(user: AuthenticateUser) -> Customer:
    return None


@customers_router.put(
    "/current",
    response_model=None,
    summary="Обновить текущего авторизованного клиента",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def put_current_customer(
    user: AuthenticateUser,
    session: DbSession,
) -> Customer:
    return None


@customers_router.get(
    "/coach",
    response_model=None,
    summary="Получение своего тренера",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_coach(
    user: AuthenticateUser,
    session: DbSession,
) -> Coach:
    return None


@customers_router.get(
    "/workouts",
    response_model=None,
    summary="Получение своих тренеровок",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_workout(
    user: AuthenticateUser,
    session: DbSession,
):
    return None


@customers_router.post(
    "/status",
    response_model=None,
    summary="Изменение прогресса задания",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def set_exercise_status(
    user: AuthenticateUser,
    session: DbSession,
):
    return None


# Для тренера
@customers_router.get(
    "/own",
    response_model=None,
    summary="Получить список клиентов, относящихся к этому тренера",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_own_customers(
    session: DbSession,
    user: AuthenticateUser,
) -> list[Customer]:
    return None


# Для тренера
@customers_router.get(
    "/free",
    response_model=None,
    summary="Получить список клиентов, не относящихся тренерам",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def get_free_customers(
    session: DbSession,
    user: AuthenticateUser,
) -> list[Customer]:
    return None


# Для тренера
@customers_router.post(
    "/assign/{customer_id}",
    response_model=None,
    summary="Назначение клиента себе",
    dependencies=[Depends(HasPermission(Authenticated()))],
)
async def assign_customers(
    session: DbSession,
    user: AuthenticateUser,
    customer_id: Annotated[int, Path],
) -> Customer:
    return None
