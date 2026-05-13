# główny plik aplikacji FastAPI

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TODO Frontend API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(tasks.router)

# static musi być na końcu
app.mount("/", StaticFiles(directory="static", html=True), name="static")