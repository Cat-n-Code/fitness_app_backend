from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fitness_app.core.db_manager import Base


class FileEntity(Base):
    __tablename__ = "file_entities"

    id: Mapped[int] = mapped_column(primary_key=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"))
    filename: Mapped[str] = mapped_column(unique=True, nullable=False)

    exercise: Mapped["Exercise"] = relationship(back_populates="photos")
