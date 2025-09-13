import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://campus:campus@db:5432/campus_jobs",  # дефолт для docker-compose
)

class Base(DeclarativeBase): ...
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# не забудь оставить get_db, если он у тебя есть
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
