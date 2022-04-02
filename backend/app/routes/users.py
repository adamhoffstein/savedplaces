from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connector import get_db
from app.services import login
from app.services.crud import users
from app.database import schemas
from app.resources.exceptions.users import (
    EMAIL_USERNAME_ALREADY_REGISTERED,
    EMAIL_ALREADY_REGISTERED,
    USERNAME_ALREADY_REGISTERED,
)

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_email = users.get_by_email(db, email=user.email)
    db_user_name = users.get_by_username(db, username=user.username)
    if db_user_email and db_user_name:
        raise EMAIL_USERNAME_ALREADY_REGISTERED
    elif db_user_email:
        raise EMAIL_ALREADY_REGISTERED
    elif db_user_name:
        raise USERNAME_ALREADY_REGISTERED
    user.hashed_password = login.get_password_hash(user.hashed_password)
    return users.create(db, user)


@router.get("/all", response_model=List[schemas.User])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(login.user_logged_in),
):
    return users.get_all(db, current_user)


@router.get("/", response_model=schemas.User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(login.user_logged_in),
):
    return users.get(db, user_id, current_user)


@router.delete("/", response_model=schemas.User)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(login.user_logged_in),
):
    return users.delete(db, user_id, current_user)


@router.put("/", response_model=schemas.User)
def update_user(
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(login.user_logged_in),
):
    return users.put(db, user, current_user)
