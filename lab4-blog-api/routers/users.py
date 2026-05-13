# router do obsługi użytkowników

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from models.post import Post
from schemas.user import UserOut, UserUpdate, PasswordChange
from schemas.post import PostOut
from auth.deps import get_current_user
from auth.security import verify_password, hash_password

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserOut)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if data.username is not None:
        existing_user = db.query(User).filter(User.username == data.username).first()

        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409,
                detail="Nazwa użytkownika już jest zajęta"
            )

        current_user.username = data.username

    if data.email is not None:
        existing_email = db.query(User).filter(User.email == data.email).first()

        if existing_email and existing_email.id != current_user.id:
            raise HTTPException(
                status_code=409,
                detail="Email już jest zajęty"
            )

        current_user.email = data.email

    db.commit()
    db.refresh(current_user)

    return current_user


@router.post("/me/change-password")
def change_password(
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Stare hasło jest niepoprawne"
        )

    current_user.hashed_password = hash_password(data.new_password)

    db.commit()

    return {
        "message": "Hasło zostało zmienione"
    }


@router.get("/{user_id}/posts", response_model=list[PostOut])
def get_user_posts(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Nie znaleziono użytkownika"
        )

    posts = db.query(Post).filter(
        Post.author_id == user_id,
        Post.published == True
    ).all()

    return posts