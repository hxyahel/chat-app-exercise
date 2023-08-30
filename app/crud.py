from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Conversation, User


def create_user(db: Session, user_id: str) -> User:
    db_user = db.query(User).filter_by(user_id=user_id).one_or_none()
    if db_user is None:
        db_user = User(user_id=user_id)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(f"Create user: {user_id}")
    return db_user


def create_conversation(db: Session, conversation: Conversation) -> Conversation:
    db_message = Conversation(user_id=conversation.user_id, text=conversation.text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_conversations_by_user(db: Session, user_id: str) -> Sequence[Conversation]:
    query = select(Conversation).where(Conversation.user_id == user_id)
    result = db.execute(query)
    return result.scalars().all()


def get_users_by_keyword(db: Session, keyword: str) -> Sequence[str]:
    query = select(User.user_id).where(User.words.ilike(f"%{keyword}%"))
    result = db.execute(query)
    return result.scalars().all()


def update_user_words(db: Session, user_id: str, new_words: str) -> User:
    db_user = db.query(User).where(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    updated_words = _keep_unique_words(db_user.words + new_words)

    db.query(User).where(User.user_id == user_id).update({"words": updated_words})
    db.commit()
    db.refresh(db_user)
    return db_user


def _keep_unique_words(text: str) -> str:
    words = text.split()
    return " ".join(set(words))
