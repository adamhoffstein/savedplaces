from sqlalchemy.orm import Session
from app.database import models, schemas


def create(db: Session, user: schemas.UserCreate):
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


def get(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()