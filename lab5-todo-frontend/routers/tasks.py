# router do obsługi zadań

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskOut

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.get("/")
def list_tasks(
    done: bool | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Task)

    if done is not None:
        query = query.filter(Task.done == done)

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            Task.title.ilike(pattern) | Task.description.ilike(pattern)
        )

    total = query.count()

    items = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
        "items": [TaskOut.model_validate(task) for task in items]
    }


@router.post("/", response_model=TaskOut, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        title=data.title,
        description=data.description
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Nie znaleziono zadania"
        )

    update_data = data.model_dump(exclude_none=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Nie znaleziono zadania"
        )

    db.delete(task)
    db.commit()