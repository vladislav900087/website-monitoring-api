from collections.abc import Iterator
from app.database.session import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError


from app.services.authentication import AuthService


bearer = OAuth2PasswordBearer(tokenUrl='monitoring-api/auth/login')

def get_db() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db=db)

def get_current_user(token: str = Depends(bearer), service: AuthService = Depends(get_auth_service)):
    try:
        return service.decode_token(token)
    except (InvalidTokenError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc



