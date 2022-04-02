from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.database import models, schemas
from app.resources.exceptions.users import (
    USER_INCORRECT_PERMISSIONS,
    USER_NOT_EXIST,
)


def create(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        email=user.email,
        hashed_password=user.hashed_password,
        username=user.username,
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    if db_user.id == 1:
        db_user.super_admin = True
        db.commit()
        db.refresh(db_user)
    return db_user


def put(
    db: Session,
    info_to_update: schemas.UserUpdate,
    logged_in_user: models.User,
) -> models.User:
    if user_in_db := get(db, info_to_update.id, logged_in_user):
        if logged_in_user != user_in_db:
            raise USER_INCORRECT_PERMISSIONS
        for key, value in info_to_update.__dict__.items():
            setattr(user_in_db, key, value)
        user_in_db.updated_date = datetime.utcnow()
        db.commit()
        db.refresh(user_in_db)
        return user_in_db
    raise USER_NOT_EXIST


def get(db: Session, user_id: int, logged_in_user) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def delete(db: Session, user_id: int, logged_in_user) -> models.User:
    user = get(db, user_id)
    db.delete(user)
    db.commit()
    return user


def get_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_by_username(db: Session, username: str) -> models.User:
    return (
        db.query(models.User).filter(models.User.username == username).first()
    )


def get_all(db: Session, logged_in_user) -> List[models.User]:
    return db.query(models.User).all()
