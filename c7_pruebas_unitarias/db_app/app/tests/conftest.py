import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy_utils import database_exists, create_database, drop_database

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_database():

    if database_exists(SQLALCHEMY_DATABASE_URL):
        drop_database(SQLALCHEMY_DATABASE_URL)
    create_database(SQLALCHEMY_DATABASE_URL)

    Base.metadata.create_all(engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    drop_database(SQLALCHEMY_DATABASE_URL)


@pytest.fixture
def test_db_session():
    session = Session(bind=engine)
    yield session

    for table in reversed(Base.metadata.sorted_tables):
        engine.connect().execute(table.delete())
    session.close()


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
