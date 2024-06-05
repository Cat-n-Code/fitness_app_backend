from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fitness_app.coaches.models import Coach
from fitness_app.core.db_manager import Base
from fitness_app.core.utils import NonEmptyStr
from fitness_app.customers.models import Customer
from fitness_app.users.schemas import Role, Sex


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[NonEmptyStr] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    sex: Mapped[Optional[Sex]] = mapped_column(nullable=True)
    birth_date: Mapped[Optional[date]] = mapped_column(nullable=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    role: Mapped[Role] = mapped_column(
        server_default="CUSTOMER", default="CUSTOMER", nullable=False
    )

    customer_info: Mapped[Optional["Customer"]] = relationship(
        "Customer", back_populates="user"
    )
    coach_info: Mapped[Optional["Coach"]] = relationship("Coach", back_populates="user")

    __table_args__ = (UniqueConstraint(email),)


class CoachesCustomers(Base):
    __tablename__ = "coaches_customers"

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), primary_key=True
    )
    coach_id: Mapped[int] = mapped_column(ForeignKey("coaches.id"), primary_key=True)
