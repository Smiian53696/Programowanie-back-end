from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db" # adres bazy danych


engine = create_engine( #tworzenie silnika bazy danych
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker( #konfiguracja sesji
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base() # baza dla modeli

#funkcja do pobierania sesji bazy danych
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()