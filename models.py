from sqlalchemy import Column, Integer, String, Boolean
from database import Base
from pydantic import BaseModel

class URLCreate(BaseModel):
    target_url: str

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String, index=True, unique=True)
    short_url = Column(String, index=True, unique=True)
    is_active = Column(Boolean, default=True)
