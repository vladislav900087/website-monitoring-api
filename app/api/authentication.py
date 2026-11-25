from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.api.dependencies import get_auth_service, get_current_user
from app.services.authentication import AuthService
from typing import Annotated
from app.models.user import User

from app.schemas.user import UserCreate, UserRead, Token




router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post('/login', response_model=Token, status_code=status.HTTP_200_OK)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], service: AuthService = Depends(get_auth_service)):
    try:
        return service.login_user(email=form.username, password=form.password)

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc), headers={'WWW-Authenticate': "Bearer"})

@router.post('/register', response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, service: AuthService = Depends(get_auth_service)):
    try:
        return service.create_user(email=data.email, password=data.password)
    except ValueError as exc:
        if 'already exists' in str(exc):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))



@router.get('/me', response_model=UserRead, status_code=status.HTTP_200_OK)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
