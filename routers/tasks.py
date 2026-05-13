# router do obsługi zadań
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from database import get_db
from models.task import Task

router = APIRouter( #konfiguracja routera
    prefix="/tasks",
    tags=["tasks"]
)



class TaskCreate(BaseModel): # model do tworzenia zadania
    title: str
    description: str = ""


#model odpowiedzi API
class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    done: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


#pobieranie wszystkich taskow
@router.get("/", response_model=list[TaskOut])
def list_tasks(
    done: bool | None = Query(None),
    search: str | None = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Task)

#filtrowanie po statusie
    if done is not None:
        query = query.filter(Task.done == done)

 #wyszukiwanie po tytule
    if search:
        query = query.filter(
            Task.title.ilike(f"%{search}%")
        )

    return query.all()



@router.get("/{task_id}", response_model=TaskOut) # pobieranie jednego zadania
def get_task(task_id: int, db: Session = Depends(get_db)):

    task = db.get(Task, task_id)

    
    if not task: # sprawdzenie czy zadanie istnieje
        raise HTTPException(
            status_code=404,
            detail="Nie znaleziono zadania"
        )

    return task


# tworzenie nowego zadania
@router.post("/", response_model=TaskOut, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):

    # tworzenie obiektu zadania
    task = Task(
        title=data.title,
        description=data.description
    )

    # zapis do bazy
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.put("/{task_id}", response_model=TaskOut) # aktualizacja task
def update_task(
    task_id: int,
    data: TaskCreate,
    db: Session = Depends(get_db)
):

    task = db.get(Task, task_id)

    if not task: # sprawdzenie czy zadanie istnieje
        raise HTTPException(
            status_code=404,
            detail="Nie znaleziono zadania"
        )

    
    task.title = data.title  # aktualizacja danych
    task.description = data.description

    db.commit()
    db.refresh(task)

    return task


@router.patch("/{task_id}/toggle", response_model=TaskOut) # zmiana statusu done
def toggle_task(task_id: int, db: Session = Depends(get_db)):

    task = db.get(Task, task_id)

   
    if not task: # sprawdzenie czy zadanie istnieje
        raise HTTPException(
            status_code=404,
            detail="Nie znaleziono zadania"
        )

    
    task.done = not task.done # zmiana true/false

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=204) # usuwanie task
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task = db.get(Task, task_id)

    if not task: # sprawdzenie czy zadanie istnieje
        raise HTTPException(
            status_code=404,
            detail="Nie znaleziono zadania"
        )


    db.delete(task)  # usunięcie z bazy
    db.commit()