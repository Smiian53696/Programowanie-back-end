from fastapi import FastAPI
from database import engine, Base
from models import task
from routers import tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TODO API",
    version="1.0"
)

app.include_router(tasks.router)