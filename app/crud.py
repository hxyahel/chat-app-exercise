from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.models import Conversation, User


def create_conversation(db: Session, user_id: str, text: str) -> Conversation:
    db_message = Conversation(user_id=user_id, text=text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_conversations_by_user(db: Session, user: str):
    stmt = select(Conversation).where(Conversation.user_id == user)
    result = db.execute(stmt)
    return result.scalars().all()


def get_users_by_keyword(db: Session, keyword: str):
    stmt = select(User.user_id).where(User.words.ilike(f"%{keyword}%"))
    result = db.execute(stmt)
    return result.scalars().all()
