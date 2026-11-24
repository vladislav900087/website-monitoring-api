from collections.abc import Iterator
from app.database.session import SessionLocal, engine
from sqlalchemy.orm import Session

def get_db() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session
