from typing import List
from sqlalchemy.orm import Session
from app.database import models, schemas
from app.services.crud.common import update_object
from app.resources.exceptions.users import (
    USER_INCORRECT_PERMISSIONS,
    USER_NOT_EXIST,
)


def create(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user

    Parameters:
    db (Session): database session
    user (schemas.UserCreate): information for the new user to create

    Returns:
    models.User: the newly created user
    """
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
    """Update a user

    Parameters:
    db (Session): database session
    info_to_update (schemas.UserUpdate): information for the user to update
    logged_in_user (models.User): the current logged in user

    Returns:
    models.User: the updated user
    """
    if user_in_db := get(db, info_to_update.id, logged_in_user):
        if logged_in_user != user_in_db:
            raise USER_INCORRECT_PERMISSIONS
        return update_object(
            db=db, info_to_update=info_to_update, object_in_db=user_in_db
        )
    raise USER_NOT_EXIST


def get(db: Session, user_id: int, logged_in_user: models.User) -> models.User:
    """Get user

    Parameters:
    db (Session): database session
    user_id (int): the user_id of the user to retrieve
    logged_in_user (models.User): the current logged in user

    Returns:
    models.User: the user in the database
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def delete(
    db: Session, user_id: int, logged_in_user: models.User
) -> models.User:
    """Delete user

    Parameters:
    db (Session): database session
    user_id (int): the user_id of the user to delete
    logged_in_user (models.User): the current logged in user

    Returns:
    models.User: the deleted user
    """
    user = get(db, user_id)
    db.delete(user)
    db.commit()
    return user


def get_by_email(db: Session, email: str) -> models.User:
    """Get user by email

    Parameters:
    db (Session): database session
    email (string): the email of the user to retrieve

    Returns:
    models.User: the user in the database
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_by_username(db: Session, username: str) -> models.User:
    """Get user by username

    Parameters:
    db (Session): database session
    username (string): the username of the user to retrieve

    Returns:
    models.User: the user in the database
    """
    return (
        db.query(models.User).filter(models.User.username == username).first()
    )


def get_all(db: Session, logged_in_user: models.User) -> List[models.User]:
    """Get all users

    Parameters:
    db (Session): database session
    logged_in_user (models.User): the current logged in user

    Returns:
    List[models.User]: a list of users in the database
    """
    return db.query(models.User).all()
