from fastapi import FastAPI
from .database import Base, engine, SessionLocal
from . import models, schemas, chatbot

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/chat")
def chat(request: schemas.ChatRequest):

    db = SessionLocal()

    user_msg = models.Message(
        session_id=request.session_id,
        role="user",
        content=request.message
    )

    db.add(user_msg)
    db.commit()

    messages = db.query(models.Message).filter(
        models.Message.session_id == request.session_id
    ).all()

    history = [
        {"role": m.role, "content": m.content}
        for m in messages
    ]

    reply = chatbot.generate_reply(history)

    ai_msg = models.Message(
        session_id=request.session_id,
        role="assistant",
        content=reply
    )

    db.add(ai_msg)
    db.commit()

    return {"reply": reply}


@app.get("/history/{session_id}")
def get_history(session_id: str):

    db = SessionLocal()

    messages = db.query(models.Message).filter(
        models.Message.session_id == session_id
    ).all()

    return messages