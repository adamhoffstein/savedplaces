from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.services.crud import users
from app.core.config import get_app_settings
from app.database import models
from app.database.connector import get_db
from app.database.schemas.jwt import Token, TokenData
from app.resources.exceptions.users import (
    USER_INACTIVE,
    USER_CREDENTIALS_EXCEPTION,
)

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SETTINGS = get_app_settings()
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a user's password

    Parameters:
    plain_password (string): the password of the user
    hashed_password (string): the hashed password of the user

    Returns:
    bool: whether or not the password has been verified
    """
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Verify a user's password

    Parameters:
    plain_password (string): the username of the user

    Returns:
    string: the hashed password of the user
    """
    return PWD_CONTEXT.hash(password)


def authenticate_user(db, username: str, password: str) -> models.User:
    """Authenticate a user

    Parameters:
    db (Session): database session
    username (string): the username of the user
    password (string): the password of the user

    Returns:
    models.User: the authenticated user in the database
    """
    user = users.get_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_token(user) -> Token:
    """Create access / refresh tokens

    Parameters:
    user (models.User): the user to create a token for

    Returns:
    schemas.Token: the auth token
    """
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


def create_encoded_jwt(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """Encode JWT data

    Parameters:
    data (dict): the data to encode
    expires_delta (timedelta): when the data should expire

    Returns:
    string: the encoded jwt string
    """
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


async def get_current_user(
    token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(get_db)
) -> models.User:
    """Determine which user is logged in

    Parameters:
    db (Session): database session
    token (string): auth token passed by the user

    Returns:
    models.User: the user in the database
    """
    try:
        payload = jwt.decode(
            token, SETTINGS.secret_key, algorithms=[SETTINGS.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise USER_CREDENTIALS_EXCEPTION
        token_data = TokenData(username=username)
    except JWTError:
        raise USER_CREDENTIALS_EXCEPTION
    user = users.get_by_username(db, username=token_data.username)
    if user is None:
        raise USER_CREDENTIALS_EXCEPTION
    return user


async def user_logged_in(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """Determine whether or not a user is logged in

    Parameters:
    current_user (models.User): logged in the user

    Returns:
    models.User: the user in the database
    """
    if current_user.disabled:
        raise USER_INACTIVE
    return current_user
