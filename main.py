import os
import openai

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import crud
from app.session import get_db
from app.schemas import UserCreate, ConversationCreate, MessageBase, UserUpdate, ConversationResponse, UserResponse

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI()


@app.post("/users", status_code=201, response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user.user_id)
    return db_user


@app.post("/chat")
def get_chatgpt_response(message: MessageBase) -> str:
    messages = [{"role": "user", "content": message.prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )
    completion = response.choices[0].message["content"]
    return completion


@app.post("/conversation/", status_code=201, response_model=ConversationResponse)
def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    db_message = crud.create_conversation(db, conversation.user_id, conversation.text)
    return db_message


@app.get("/conversations/{user}", status_code=200)
def get_conversations_by_user(user: str, db: Session = Depends(get_db)):
    conversations_by_user = crud.get_conversations_by_user(db, user)
    return conversations_by_user


@app.get("/users/{keyword}", status_code=200)
def get_users_by_keyword(keyword: str, db: Session = Depends(get_db)):
    users_by_keyword = crud.get_users_by_keyword(db, keyword)
    return users_by_keyword


@app.put("/users/{user_id}", status_code=200, response_model=UserResponse)
def update_user_words(user_id: str, words: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user_words(db, user_id, words.words)
    return db_user
