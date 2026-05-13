# router do obsługi komentarzy

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.comment import Comment
from models.post import Post
from models.user import User
from schemas.comment import CommentCreate, CommentOut
from auth.deps import get_current_user

router = APIRouter(
    tags=["comments"]
)


@router.get("/posts/{post_id}/comments", response_model=list[CommentOut])
def list_comments(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.get(Post, post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Nie znaleziono posta"
        )

    return db.query(Comment).filter(Comment.post_id == post_id).all()


@router.post("/posts/{post_id}/comments", response_model=CommentOut, status_code=201)
def create_comment(
    post_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.get(Post, post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Nie znaleziono posta"
        )

    comment = Comment(
        content=data.content,
        post_id=post_id,
        author_id=current_user.id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


@router.delete("/comments/{comment_id}", status_code=204)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = db.get(Comment, comment_id)

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Nie znaleziono komentarza"
        )

    if current_user.role != "admin" and comment.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Brak uprawnień do usunięcia tego komentarza"
        )

    db.delete(comment)
    db.commit()