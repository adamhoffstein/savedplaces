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
    placelist_name: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(login.user_logged_in),
):
    return placelists.create(db, placelist_name, current_user)


@router.post("/append", response_model=schemas.PlaceList)
def append_placelist(
    place_id: int,
    placelist_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(login.user_logged_in),
):
    return placelists.add(
        db=db,
        placelist_id=placelist_id,
        place_id=place_id,
        logged_in_user=current_user,
    )


@router.post("/remove", response_model=schemas.PlaceList)
def remove_placelist(
    place_id: int,
    placelist_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(login.user_logged_in),
):
    return placelists.remove(
        db=db,
        placelist_id=placelist_id,
        place_id=place_id,
        logged_in_user=current_user,
    )


@router.get("/all", response_model=List[schemas.PlaceList])
def get_all_placelists(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(login.user_logged_in),
):
    return placelists.get_all(db, current_user)


@router.get("/", response_model=schemas.PlaceList)
def get_placelist(
    placelist_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(login.user_logged_in),
):
    return placelists.get(db, placelist_id, current_user)


@router.delete("/", response_model=schemas.PlaceList)
def delete_placelist(
    placelist_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(login.user_logged_in),
):
    return placelists.delete(db, placelist_id, current_user)


@router.put("/", response_model=schemas.PlaceList)
def update_placelist(
    placelist: schemas.PlaceListUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(login.user_logged_in),
):
    return placelists.put(db, placelist, current_user)
