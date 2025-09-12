# backend/tests/conftest.py
import sys, os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest

# чтобы работал from app import ...
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.db import Base, get_db
from app import models

# --- ИСПРАВЛЕНО: in-memory SQLite + StaticPool (без файлов и блокировок) ---
engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,        # одна память для всех соединений
    future=True,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Перед каждым тестом создаём чистые таблицы, после — дропаем
@pytest.fixture(autouse=True)
def _db_clean():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def make_vacancy():
    def _make():
        db = TestingSessionLocal()
        org = models.Organization(name="Test Org")
        db.add(org); db.flush()
        vac = models.Vacancy(
            org_id=org.id,
            title="Junior Developer",
            description="Great opportunity",
            employment_type="full-time",
            location="Remote",
            is_active=True,
        )
        db.add(vac)
        db.commit()
        vid = vac.id
        db.close()
        return vid
    return _make
