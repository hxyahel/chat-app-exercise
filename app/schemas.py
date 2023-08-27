from datetime import datetime
from typing import List

from pydantic import BaseModel


class ConversationBase(BaseModel):
    user_id: str
    text: str


class ConversationCreate(ConversationBase):
    pass


class ConversationResponse(ConversationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ConversationSearchResult(BaseModel):
    conversations: List[ConversationResponse]


class UserCreate(BaseModel):
    user_id: str


class UserUpdate(BaseModel):
    words: str


class UserResponse(UserCreate):
    words: str

    class Config:
        orm_mode = True


class UserSearchResult(BaseModel):
    users: List[str]


class MessageBase(BaseModel):
    prompt: str
