# główny plik aplikacji FastAPI

from fastapi import FastAPI

from database import engine, Base
from models import user, post, comment, tag
from routers import auth, users, posts, comments, tags

# tworzenie tabel w bazie danych
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog API",
    version="1.0"
)


@app.get("/")
def root():
    return {
        "message": "Blog API is working"
    }


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(tags.router)