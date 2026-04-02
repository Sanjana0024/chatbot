from sqlalchemy import Column, Integer, String
from database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String)
    role = Column(String)
    content = Column(String)
  