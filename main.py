import os
import openai

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import crud
from app.database.models import User, get_db
from app.schemas import UserCreate, ConversationCreate, MessageBase, UserUpdate


openai.api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI()


@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_id = user.user_id
    existing_user = db.query(User).filter_by(user_id=user_id).first()
    if existing_user is None:
        db_user = User(user_id=user_id)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(f'Create user: {user_id}')
    return User(user_id=user_id)


@app.get("/chat")
def get_chatgpt_response(message: MessageBase) -> str:
    messages = [{"role": "user", "content": message.prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )
    completion = response.choices[0].message["content"]
    return completion


@app.post("/conversation/")
async def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    db_message = crud.create_conversation(db, conversation.user_id, conversation.text)
    return db_message


@app.get("/conversations/{user}")
def get_conversations_by_user(user: str, db: Session = Depends(get_db)):
    conversations_by_user = crud.get_conversations_by_user(db, user)
    return conversations_by_user


@app.get("/users/{keyword}")
def get_users_by_keyword(keyword: str, db: Session = Depends(get_db)):
    users_by_keyword = crud.get_users_by_keyword(db, keyword)
    return users_by_keyword


@app.put("/users_words", status_code=200)
def update_user_words(user: UserUpdate, db: Session = Depends(get_db)):
    def _keep_unique_words(text: str):
        words = text.split()
        return " ".join(set(words))

    user_record = db.query(User).filter_by(user_id=user.user_id).first()
    existing_words = user_record.words if user_record.words else ""
    updated_words = _keep_unique_words(existing_words + user.text)
    user_record.words = updated_words
    db.commit()
    return user_record.words
