# model posta

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from models.tag import post_tags


class Post(Base):
    __tablename__ = "posts"

    # id posta
    id = Column(Integer, primary_key=True, index=True)

    # tytuł posta
    title = Column(String(200), nullable=False)

    # treść posta
    content = Column(Text, nullable=False)

    # czy post jest opublikowany
    published = Column(Boolean, default=False)

    # id autora posta
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # relacja post -> użytkownik
    author = relationship(
        "User",
        back_populates="posts"
    )

    # relacja post -> komentarze
    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    # relacja post -> tagi
    tags = relationship(
        "Tag",
        secondary=post_tags,
        back_populates="posts"
    )