from collections.abc import Iterator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from app.database.base import Base
from app.api.dependencies import get_db
from app.main import app
from app.config.settings import settings


@pytest.fixture(scope='session')
def db_client() -> Iterator[Engine]:

    assert settings.database_url == 'postgresql+psycopg://test:test@test-db:5432/app_test'
    engine = create_engine(settings.database_url)

    try:
        Base.metadata.create_all(engine)
        yield engine
    finally:
        engine.dispose()

@pytest.fixture
def db_session(db_client: Engine) -> Iterator[Session]:
    with db_client.connect() as connection, connection.begin() as transaction:
        with Session(bind=connection, join_transaction_mode="create_savepoint") as session:
            yield session
        transaction.rollback()

@pytest.fixture
def client(db_session: Session) -> Iterator[TestClient]:
    app.dependency_overrides[get_db] = lambda: db_session

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)

