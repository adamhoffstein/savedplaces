from fastapi import HTTPException


PLACELIST_NOT_EXIST = HTTPException(
    status_code=400, detail="PlaceList does not exist"
)

PLACE_ALREADY_IN_PLACELIST = HTTPException(
    status_code=400, detail="Place already in PlaceList"
)

PLACE_NOT_IN_PLACELIST = HTTPException(
    status_code=400, detail="Place not in PlaceList"
)
