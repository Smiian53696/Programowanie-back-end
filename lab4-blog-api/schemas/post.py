# schematy posta

from pydantic import BaseModel
from schemas.tag import TagOut


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = False
    tag_ids: list[int] = []


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    author_id: int
    tags: list[TagOut] = []

    model_config = {
        "from_attributes": True
    }