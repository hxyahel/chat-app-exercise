from datetime import datetime
from typing import Optional

from sqlalchemy import INTEGER, Sequence, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TableNameMixin


class Conversation(Base, TableNameMixin):
    id: Mapped[int] = mapped_column(INTEGER, Sequence("conversation_id_seq"), primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.user_id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    text: Mapped[str] = mapped_column(String)

    user = relationship("User", back_populates="conversations")


class User(Base, TableNameMixin):
    user_id: Mapped[str] = mapped_column(String, index=True, unique=True, primary_key=True)
    words: Mapped[Optional[str]] = mapped_column(String)

    conversations = relationship("Conversation", back_populates="user")
