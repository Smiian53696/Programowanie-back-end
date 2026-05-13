# plik do konfiguracji bazy danych
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#połączenie z SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine( #tworzenie silnika bazy danych
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker( # konfig sesji
    bind=engine,
    autocommit=False,
    autoflush=False
)
Base = declarative_base() # SQLAlchemy

def get_db(): #funkcja do pobierania połączenia z bazą
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()