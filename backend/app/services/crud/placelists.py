from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.database import models, schemas
from app.services.crud import places
from app.resources.exceptions.placelists import (
    PLACELIST_NOT_EXIST,
    PLACE_ALREADY_IN_PLACELIST,
    PLACE_NOT_IN_PLACELIST,
)


def create(
    db: Session, placelist_name: str, logged_in_user: models.User
) -> models.PlaceList:
    """Create a new placelist

    Parameters:
    db (Session): database session
    placelist_name (string): the name of the new placelist
    logged_in_user (models.User): the current logged in user

    Returns:
    models.PlaceList: the newly created placelist
    """
    db_place_list = models.PlaceList(name=placelist_name)
    db_place_list.owner = logged_in_user
    db.add(db_place_list)
    db.commit()
    db.refresh(db_place_list)
    return db_place_list


def get(
    db: Session, placelist_id: int, logged_in_user: models.User
) -> models.PlaceList:
    """Get placelist

    Parameters:
    db (Session): database session
    placelist_id (int): the placelist_id of the placelist to retrieve
    logged_in_user (models.User): the current logged in user

    Returns:
    models.PlaceList: the placelist in the database
    """
    if (
        placelist := db.query(models.PlaceList)
        .filter(models.PlaceList.id == placelist_id)
        .first()
    ):
        return placelist
    raise PLACELIST_NOT_EXIST


def get_all(
    db: Session, logged_in_user: models.User
) -> List[models.PlaceList]:
    """Get all placelists

    Parameters:
    db (Session): database session
    logged_in_user (models.User): the current logged in user

    Returns:
    List[models.PlaceList]: a list of placelists in the database
    """
    return db.query(models.PlaceList).all()


def add(
    db: Session, placelist_id: int, place_id: int, logged_in_user: models.User
) -> models.PlaceList:
    """Add place to placelist

    Parameters:
    db (Session): database session
    placelist_id (int): the placelist_id of the placelist to modify
    plac_id (int): the place_id of the place to add
    logged_in_user (models.User): the current logged in user

    Returns:
    models.PlaceList: the placelist in the database
    """
    if place := places.get(db, place_id, logged_in_user):
        if placelist := get(db, placelist_id, logged_in_user):
            if place not in placelist.places:
                placelist.places.append(place)
                placelist.updated_date = datetime.utcnow()
                db.commit()
                db.refresh(placelist)
                return placelist
            raise PLACE_ALREADY_IN_PLACELIST


def remove(
    db: Session, placelist_id: int, place_id: int, logged_in_user: models.User
) -> models.PlaceList:
    """Remove place from placelist

    Parameters:
    db (Session): database session
    placelist_id (int): the placelist_id of the placelist to modify
    plac_id (int): the place_id of the place to remove
    logged_in_user (models.User): the current logged in user

    Returns:
    models.PlaceList: the placelist in the database
    """
    if place := places.get(db, place_id, logged_in_user):
        if placelist := get(db, placelist_id, logged_in_user):
            if place in placelist.places:
                placelist.places.remove(place)
                placelist.updated_date = datetime.utcnow()
                db.commit()
                db.refresh(placelist)
                return placelist
            raise PLACE_NOT_IN_PLACELIST


def delete(
    db: Session, placelist_id: int, logged_in_user: models.User
) -> models.PlaceList:
    """Delete placelist

    Parameters:
    db (Session): database session
    placelist_id (int): the placelist_id of the placelist to delete
    logged_in_user (models.User): the current logged in user

    Returns:
    models.PlaceList: the deleted placelist
    """
    if placelist := get(db, placelist_id):
        db.delete(placelist)
        db.commit()
        return placelist
    raise PLACELIST_NOT_EXIST


def put(
    db: Session,
    info_to_update: schemas.PlaceListUpdate,
    logged_in_user: models.User,
) -> models.PlaceList:
    """Update a placelist

    Parameters:
    db (Session): database session
    info_to_update (schemas.PlaceListUpdate): information for the placelist to update
    logged_in_user (models.User): the current logged in user

    Returns:
    models.PlaceList: the updated placelist
    """
    if placelist_in_db := get(db, info_to_update.id, logged_in_user):
        for key, value in info_to_update.__dict__.items():
            setattr(placelist_in_db, key, value)
        placelist_in_db.updated_date = datetime.utcnow()
        db.commit()
        db.refresh(placelist_in_db)
        return placelist_in_db
    raise PLACELIST_NOT_EXIST
