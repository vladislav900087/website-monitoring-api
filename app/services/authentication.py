from app.config.settings import settings
from datetime import UTC, datetime, timedelta


import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User

password_hash = PasswordHash.recommended()

secret = settings.jwt_secret_key
algorithm = "HS256"
issuer = "demo-auth"
audience = "demo-api"

unauthorized = ValueError("Invalid credentials")


def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, email: str, password: str):

        statement = select(User).where(User.email == email)

        user = self.db.scalar(statement)

        if user is not None:
            raise ValueError('User already exists')

        user = User(email=email, hashed_password=hash_password(password))

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def authenticate_user(self, email: str, password: str):

        statement = select(User).where(User.email == email)

        user = self.db.scalar(statement)

        if user is None:
            raise ValueError('User does not exist')

        if not verify_password(plain_password=password, hashed_password=user.hashed_password):
            raise unauthorized

        return user

    def login_user(self, email: str, password: str):

        user = self.authenticate_user(email, password)

        payload = {
            "sub": str(user.id),
            "exp": datetime.now(UTC) + timedelta(minutes=30),
            "iss": issuer,
            "aud": audience
        }
        token = jwt.encode(
            payload,
            secret,
            algorithm=algorithm
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    def decode_token(self, token: str) -> User:
        try:
            claims = jwt.decode(
                    token,
                    secret,
                    algorithms=[algorithm],
                    issuer=issuer,
                    audience=audience,
                    options={"require": ["sub", "exp", "iss", "aud"]}
                )
        except InvalidTokenError as exc:
            raise unauthorized

        user_id = int(claims["sub"])
        statement = select(User).where(User.id == user_id)
        user = self.db.scalar(statement)
        if user is None:
            raise unauthorized

        return user






