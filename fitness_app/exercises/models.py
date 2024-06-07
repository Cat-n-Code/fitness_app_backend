from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fitness_app.core.db_manager import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    originalUri: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=False)
    muscle: Mapped[str] = mapped_column(nullable=True)
    additionalMuscle: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[str] = mapped_column(nullable=True)
    equipment: Mapped[str] = mapped_column(nullable=True)
    difficulty: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="exercises")
    photos: Mapped[list["FileEntity"]] = relationship(
        back_populates="exercise", cascade="all, delete-orphan"
    )
