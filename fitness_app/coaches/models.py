from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fitness_app.coaches.schemas import Speciality
from fitness_app.core.db_manager import Base

if TYPE_CHECKING:
    from fitness_app.customers.models import Customer
    from fitness_app.users.models import User


class Coach(Base):
    __tablename__ = "coaches"

    id: Mapped[int] = mapped_column(primary_key=True)
    speciality: Mapped[Speciality] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="coach_info")
    customers: Mapped[list["Customer"]] = relationship(
        "Customer", back_populates="coaches", secondary="coaches_customers"
    )
