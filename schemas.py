from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: "123"
    message: "hello"