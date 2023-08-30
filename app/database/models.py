from datetime import datetime

from sqlalchemy import INTEGER, ForeignKey, Sequence, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TableNameMixin


class User(Base, TableNameMixin):
    user_id: Mapped[str] = mapped_column(String, index=True, unique=True, primary_key=True)
    words: Mapped[str] = mapped_column(String, default="")


class Conversation(Base, TableNameMixin):
    id: Mapped[int] = mapped_column(INTEGER, Sequence("conversation_id_seq"), primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("user.user_id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    text: Mapped[str] = mapped_column(String)
