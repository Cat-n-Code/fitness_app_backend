from datetime import date

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fitness_app.core.db_manager import Base
from fitness_app.users.schemas import Sex


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    sex: Mapped[Sex] = mapped_column(nullable=True)
    birth_date: Mapped[date] = mapped_column(nullable=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    customer_info: Mapped["Customer"] = relationship("Customer", back_populates="user")
    coach_info: Mapped["Coach"] = relationship("Coach", back_populates="user")

    __table_args__ = (UniqueConstraint(email),)
