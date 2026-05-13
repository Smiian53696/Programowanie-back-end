# model użytkownika
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # id użytkownika
    username = Column(String(50), unique=True, nullable=False) # nazwa użytkownika
    email = Column(String(255), unique=True, nullable=False)  # email użytkownika
    hashed_password = Column(String, nullable=False)  # zahashowane hasło
    role = Column(String(20), default="user") # rola użytkownika

    #relacja jeden użytkownik -> wiele postów
    posts = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan"
    )