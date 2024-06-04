from sqlalchemy.ext.asyncio import AsyncSession

from fitness_app.coaches.models import Coach
from fitness_app.coaches.repositories import CoachRepository
from fitness_app.coaches.schemas import (
    CoachCreateSchema,
    CoachSaveSchema,
    CoachUpdateSchema,
)
from fitness_app.core.exceptions import EntityNotFoundException
from fitness_app.core.utils import update_model_by_schema
from fitness_app.users.models import User
from fitness_app.users.repositories import UserRepository
from fitness_app.users.schemas import UserCreateSchema
from fitness_app.users.services import UserService


class CoachService:
    def __init__(
        self,
        coach_repository: CoachRepository,
        user_repository: UserRepository,
        user_service: UserService,
    ):
        self._coach_repository = coach_repository
        self._user_repository = user_repository
        self._user_service = user_service

    async def create(self, session: AsyncSession, schema: CoachCreateSchema):
        userSchema = UserCreateSchema(**schema.model_dump(exclude=["speciality"]))

        saved_user = await self._user_service.create(session, userSchema)
        coachSchema = CoachSaveSchema(
            speciality=schema.speciality,
            user_id=saved_user.id,
        )
        coach = Coach(**coachSchema.model_dump())
        setattr(coach, "user", saved_user)
        setattr(coach, "customers", [])
        setattr(saved_user, "coach_info", coach)
        self._user_repository.save(session, saved_user)
        print("user:", saved_user.coach_info)
        return await self._coach_repository.save(session, coach)

    async def get_current(self, user: User):
        print("user:", user)
        if user is None:
            raise EntityNotFoundException("User with given id was not found")
        if user.coach_info is None:
            raise EntityNotFoundException("User with given id is not a coach")
        return user.coach_info

    async def get_by_id(self, session: AsyncSession, coach_id: int):
        coach = await session.get(Coach, coach_id)
        if coach is None:
            raise EntityNotFoundException("Coach with given id was not found")

        return coach

    async def get_by_user_id(self, session: AsyncSession, user_id: int):
        user = await session.get(User, id)
        if user is None:
            raise EntityNotFoundException("User with given id was not found")
        if user.coach_info is None:
            raise EntityNotFoundException("User with given id is not a coach")

        return await user.coach_info

    async def update_by_user(
        self, session: AsyncSession, schema: CoachUpdateSchema, user: User
    ):
        coach = user.coach_info
        if coach is None:
            raise EntityNotFoundException("Coach with given id was not found")

        update_model_by_schema(coach, schema)

        return await self._coach_repository.save(session, coach)

    async def delete_by_id(self, session: AsyncSession, coach_id: int):
        coach = await session.get(Coach, coach_id)
        if coach is None:
            raise EntityNotFoundException("Coach with given id was not found")
        self._user_service.delete_by_id(session, coach.user_id)

        return await self._coach_repository.delete(session, coach)
