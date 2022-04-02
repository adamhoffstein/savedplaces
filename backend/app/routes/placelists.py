from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connector import get_db
from app.services import login
from app.services.crud import placelists
from app.database import schemas

router = APIRouter()


@router.post("/", response_model=schemas.PlaceList)
def create_place_list(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(login.user_logged_in),
):
    return placelists.create(db, current_user)


@router.get("/all", response_model=List[schemas.PlaceList])
def get_all_placelists(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(login.user_logged_in),
):
    return placelists.get_all(db, current_user)


# @router.get("/", response_model=schemas.Place)
# def get_place(
#     place_id: int,
#     db: Session = Depends(get_db),
#     current_user: schemas.User = Depends(login.user_logged_in),
# ):
#     return places.get(db, place_id, current_user)


# @router.delete("/", response_model=schemas.Place)
# def delete_place(
#     place_id: int,
#     db: Session = Depends(get_db),
#     current_user: schemas.User = Depends(login.user_logged_in),
# ):
#     return places.delete(db, place_id, current_user)


# @router.put("/", response_model=schemas.Place)
# def update_place(
#     place: schemas.PlaceUpdate,
#     db: Session = Depends(get_db),
#     current_user: schemas.User = Depends(login.user_logged_in),
# ):
#     return places.put(db, place, current_user)
