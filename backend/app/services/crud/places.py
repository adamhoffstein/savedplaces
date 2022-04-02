from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.database import models, schemas
from app.resources.exceptions.places import (
    PLACE_ALREADY_EXISTS,
    PLACE_NOT_EXIST,
)


def get_by_google_place_id(db: Session, google_place_id: str) -> models.Place:
    return (
        db.query(models.Place)
        .filter(models.Place.google_place_id == google_place_id)
        .first()
    )


def create(
    db: Session, place: schemas.PlaceBase, logged_in_user: models.User
) -> models.Place:
    if get_by_google_place_id(db, place.google_place_id):
        raise PLACE_ALREADY_EXISTS
    db_place = models.Place(**place.__dict__)
    db_place.owner = logged_in_user
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place


def get(
    db: Session, place_id: int, logged_in_user: models.User
) -> models.Place:
    if (
        place := db.query(models.Place)
        .filter(models.Place.id == place_id)
        .first()
    ):
        return place
    raise PLACE_NOT_EXIST


def get_all(db: Session, logged_in_user: models.User) -> List[models.Place]:
    return db.query(models.Place).all()


def delete(
    db: Session, place_id: int, logged_in_user: models.User
) -> models.Place:
    if place := get(db, place_id):
        db.delete(place)
        db.commit()
        return place
    raise PLACE_NOT_EXIST


def put(
    db: Session,
    info_to_update: schemas.PlaceUpdate,
    logged_in_user: models.User,
) -> models.Place:
    if place_in_db := get(db, info_to_update.id, logged_in_user):
        for key, value in info_to_update.__dict__.items():
            setattr(place_in_db, key, value)
        place_in_db.updated_date = datetime.utcnow()
        db.commit()
        db.refresh(place_in_db)
        return place_in_db
    raise PLACE_NOT_EXIST
