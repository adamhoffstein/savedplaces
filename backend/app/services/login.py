from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.services.crud import users
from app.core.config import get_app_settings
from app.database import models
from app.database.schemas.jwt import Token

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SETTINGS = get_app_settings()


def verify_password(plain_password: str, hashed_password: str) -> str:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def authenticate_user(db, username: str, password: str) -> models.User:
    user = users.get_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_token(user) -> Token:
    access_token_expires = timedelta(
        minutes=SETTINGS.access_token_expire_minutes
    )
    refresh_token_expires = timedelta(
        minutes=SETTINGS.refresh_token_expire_minutes
    )

    access_token = create_encoded_jwt(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    refresh_token = create_encoded_jwt(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "super_admin": user.super_admin,
    }


def create_encoded_jwt(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SETTINGS.secret_key, algorithm=SETTINGS.algorithm
    )
    return encoded_jwt
