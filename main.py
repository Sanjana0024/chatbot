import os
from fastapi import FastAPI
from pydantic import BaseModel
from database import Base, engine, SessionLocal
from models import Conversation
from chat_functions import generate_reply
from uuid import uuid4

print(" Starting FastAPI Chatbot Server")

Base.metadata.create_all(bind=engine)

app = FastAPI()
print("FastAPI app initialized")
class ChatRequest(BaseModel):
    message: str
    session_id: str = None 
    print("ChatRequest model loaded") 

@app.get("/")
def read_root():
    return {"message": "Chatbot server is running!"}


@app.post("/chat")
def chat(request: ChatRequest):

    print(" New Chat Request Received")

    print("User Message:", request.message)
    print("Session ID from request:", request.session_id)
   
    session_id = request.session_id or str(uuid4())

    print(" Opening database session")
    db = SessionLocal()
    try:

        print("fetch previous conversation from database")

        messages = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).order_by(Conversation.timestamp).all()

        print("Previous Messages Found:", len(messages))

        history = [{"role": m.role, "content": m.content} for m in messages]
        print("Conversation History Loaded:")
        print(history)

        history.append({"role": "user", "content": request.message})
        print("Updated History Sent to AI:")
        print(history)

        
        ai_reply = generate_reply(history)
        print("AI Response Received:")
        print(ai_reply)

        print("Saving messages to database")

       
        db.add(Conversation(role="user", content=request.message, session_id=session_id))
        
        db.add(Conversation(role="assistant", content=ai_reply, session_id=session_id))
        db.commit()
        print("Messages saved successfully")

    finally:
        print("Closing database session")
        db.close()

    return {"session_id": session_id, "reply": ai_reply}


@app.get("/history/{session_id}")
def get_history(session_id: str):

    print("Fetching conversation history")
    print("session_id:", session_id)

    db = SessionLocal()
    try:
        messages = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).order_by(Conversation.timestamp).all()
        print("Messages Found:", len(messages))

        return [
            {"role": m.role, "content": m.content, "timestamp": m.timestamp.isoformat()}
            for m in messages
        ]
        print("Returning history to client")
    finally:
        print("closing database sess")
        db.close()