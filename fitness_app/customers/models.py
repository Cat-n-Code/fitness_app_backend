from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fitness_app.core.db_manager import Base

if TYPE_CHECKING:
    from fitness_app.coaches.models import Coach
    from fitness_app.users.models import User


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="customer_info")

    coach_id: Mapped[int] = mapped_column(ForeignKey("coaches.id"), nullable=False)
    coach: Mapped["Coach"] = relationship(back_populates="customers")
