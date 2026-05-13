# router do obsługi postów

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models.post import Post
from models.tag import Tag
from models.user import User
from schemas.post import PostCreate, PostOut
from auth.deps import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


# pobieranie postów z filtrowaniem i wyszukiwaniem
@router.get("/", response_model=list[PostOut])
def list_posts(
    tag: str | None = Query(None),
    search: str | None = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Post).filter(Post.published == True)

    # filtrowanie po tagu
    if tag:
        query = query.join(Post.tags).filter(Tag.name == tag)

    # wyszukiwanie w tytule i treści
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            Post.title.ilike(pattern) | Post.content.ilike(pattern)
        )

    return query.all()


# pobieranie jednego posta
@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):

    post = db.get(Post, post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Nie znaleziono posta"
        )

    return post


# tworzenie posta przez zalogowanego użytkownika
@router.post("/", response_model=PostOut, status_code=201)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = Post(
        title=data.title,
        content=data.content,
        published=data.published,
        author_id=current_user.id
    )

    # przypisanie tagów do posta
    if data.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()

        if len(tags) != len(data.tag_ids):
            raise HTTPException(
                status_code=404,
                detail="Niektóre tagi nie istnieją"
            )

        post.tags = tags

    db.add(post)
    db.commit()
    db.refresh(post)

    return post