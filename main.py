import os
from fastapi import FastAPI
from pydantic import BaseModel
from database import Base, engine, SessionLocal
from models import Conversation
from chat_functions import generate_reply
from uuid import uuid4


Base.metadata.create_all(bind=engine)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    session_id: str = None  # optional; generate if not provided

@app.get("/")
def read_root():
    return {"message": "Chatbot server is running!"}


@app.post("/chat")
def chat(request: ChatRequest):
   
    session_id = request.session_id or str(uuid4())

   
    db = SessionLocal()
    try:
        messages = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).order_by(Conversation.timestamp).all()

        history = [{"role": m.role, "content": m.content} for m in messages]

       
        history.append({"role": "user", "content": request.message})

        
        ai_reply = generate_reply(history)

       
        db.add(Conversation(role="user", content=request.message, session_id=session_id))
        
        db.add(Conversation(role="assistant", content=ai_reply, session_id=session_id))
        db.commit()

    finally:
        db.close()

    return {"session_id": session_id, "reply": ai_reply}


@app.get("/history/{session_id}")
def get_history(session_id: str):
    db = SessionLocal()
    try:
        messages = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).order_by(Conversation.timestamp).all()

        return [
            {"role": m.role, "content": m.content, "timestamp": m.timestamp.isoformat()}
            for m in messages
        ]
    finally:
        db.close()