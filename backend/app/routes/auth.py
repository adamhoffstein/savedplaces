from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.connector import get_db
from app.database.schemas.jwt import Token
from app.resources.exceptions.users import USER_CREDENTIALS_EXCEPTION
from app.services import login

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = login.authenticate_user(db, form_data.username, form_data.password)
    if user:
        return login.create_token(user)
    raise USER_CREDENTIALS_EXCEPTION
