from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from database import Base

class Task(Base): # model zadania
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True) # id zadania
    title = Column(String(200), nullable=False) # tytuł zadania
    description = Column(String(1000), default="") # opis zadania
    done = Column(Boolean, default=False)  # status wykonania
    created_at = Column(DateTime, default=datetime.utcnow) # data utworzenia