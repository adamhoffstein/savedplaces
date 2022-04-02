from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.database import models, schemas
from app.services.crud import places


def create(db: Session, logged_in_user: models.User) -> models.PlaceList:
    places_in_db = places.get_all(db, logged_in_user)
    print("places", places_in_db)
    db_place_list = models.PlaceList(name="Hello")
    db_place_list.assigned_places = (places_in_db,)
    db_place_list.owner = logged_in_user
    db.add(db_place_list)
    db.commit()
    db.refresh(db_place_list)
    return db_place_list


def get_all(
    db: Session, logged_in_user: models.User
) -> List[models.PlaceList]:
    return db.query(models.PlaceList).all()
