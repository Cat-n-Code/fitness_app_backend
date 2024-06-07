from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fitness_app.core.db_manager import Base
from fitness_app.users.models import User

if TYPE_CHECKING:
    from fitness_app.messages.models import Message


class Chat(Base):
    __tablename__ = "chats"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    last_timestamp: Mapped[datetime] = mapped_column(
        default=datetime.now, server_default=func.now()
    )

    users: Mapped[list["User"]] = relationship(
        "User", back_populates="chats", secondary="chats_users"
    )
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat")


class ChatsUsers(Base):
    __tablename__ = "chats_users"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
