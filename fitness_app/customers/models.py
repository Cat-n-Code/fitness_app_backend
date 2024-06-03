from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from fitness_app.core.db_manager import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
