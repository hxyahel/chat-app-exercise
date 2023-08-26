from pydantic import BaseModel


class ConversationCreate(BaseModel):
    user_id: str
    text: str


class UserCreate(BaseModel):
    user_id: str


class MessageBase(BaseModel):
    prompt: str


class UserUpdate(UserCreate):
    text: str
