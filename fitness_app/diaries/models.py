from datetime import date

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fitness_app.core.db_manager import Base
from fitness_app.users.models import User


class DiaryEntry(Base):
    __tablename__ = "diaries_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    feeling: Mapped[str] = mapped_column()
    date_field: Mapped[date] = mapped_column()

    user: Mapped["User"] = relationship(back_populates="diaries")

    __table_args__ = (
        UniqueConstraint("user_id", "date_field", name="uq_diary_user_date"),
    )
