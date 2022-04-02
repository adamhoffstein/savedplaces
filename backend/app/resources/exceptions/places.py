from fastapi import HTTPException


PLACE_ALREADY_EXISTS = HTTPException(
    status_code=400, detail="The Google Place ID is already registered."
)

PLACE_NOT_EXIST = HTTPException(status_code=400, detail="Place does not exist")
