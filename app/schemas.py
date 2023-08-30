from datetime import datetime

from pydantic import BaseModel


class ConversationBase(BaseModel):
    user_id: str
    text: str


class NewConversation(ConversationBase):
    pass


class ConversationResponse(ConversationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ConversationSearchResult(BaseModel):
    conversations: list[ConversationResponse]


class UserCreate(BaseModel):
    user_id: str


class UserUpdate(BaseModel):
    words: str


class UserResponse(UserCreate):
    words: str

    class Config:
        orm_mode = True


class UserSearchResult(BaseModel):
    users: list[str]


class MessageBase(BaseModel):
    prompt: str
