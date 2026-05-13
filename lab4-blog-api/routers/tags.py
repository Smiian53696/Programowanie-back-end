# router do obsługi tagów

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.tag import Tag
from models.user import User
from schemas.tag import TagCreate, TagOut
from auth.deps import get_current_user

router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)


@router.get("/", response_model=list[TagOut])
def list_tags(db: Session = Depends(get_db)):
    # pobieranie wszystkich tagów
    return db.query(Tag).all()


@router.post("/", response_model=TagOut, status_code=201)
def create_tag(
    data: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # tylko admin może dodawać tagi
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Tylko admin może dodawać tagi"
        )

    # sprawdzenie czy tag już istnieje
    if db.query(Tag).filter(Tag.name == data.name).first():
        raise HTTPException(
            status_code=409,
            detail="Tag już istnieje"
        )

    tag = Tag(name=data.name)

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag


@router.delete("/{tag_id}", status_code=204)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # tylko admin może usuwać tagi
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Tylko admin może usuwać tagi"
        )

    tag = db.get(Tag, tag_id)

    if not tag:
        raise HTTPException(
            status_code=404,
            detail="Nie znaleziono tagu"
        )

    db.delete(tag)
    db.commit()