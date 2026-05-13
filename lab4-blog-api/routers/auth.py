# router do rejestracji i logowania

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.user import UserCreate, UserOut
from auth.security import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):

    # sprawdzenie czy email jest zajęty
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(
            status_code=409,
            detail="Email już jest zajęty"
        )

    # sprawdzenie czy username jest zajęty
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(
            status_code=409,
            detail="Nazwa użytkownika już jest zajęta"
        )

    # tworzenie nowego użytkownika
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=data.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # szukanie użytkownika po username
    user = db.query(User).filter(User.username == form_data.username).first()

    # sprawdzenie loginu i hasła
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Niepoprawna nazwa użytkownika lub hasło"
        )

    # tworzenie tokenu
    token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }