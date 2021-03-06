from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    disabled: bool
    updated_date: Optional[datetime]
    created_date: datetime
    super_admin: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    id: int
    email: EmailStr
    full_name: str


class PlaceBase(BaseModel):
    google_place_id: str
    name: str


class PlaceListSmall(BaseModel):
    id: int
    name: str
    owner: User
    updated_date: Optional[datetime]
    created_date: datetime

    class Config:
        orm_mode = True


class Place(PlaceBase):
    id: int
    updated_date: Optional[datetime]
    created_date: datetime
    owner: User
    placelists: List[PlaceListSmall]

    class Config:
        orm_mode = True


class PlaceSmall(PlaceBase):
    id: int
    updated_date: Optional[datetime]
    created_date: datetime
    owner: User
    
    class Config:
        orm_mode = True


class PlaceUpdate(BaseModel):
    id: int
    name: str


class PlaceList(BaseModel):
    id: int
    name: str
    updated_date: Optional[datetime]
    created_date: datetime
    places: Optional[List[PlaceSmall]]
    owner: User

    class Config:
        orm_mode = True


class PlaceListUpdate(BaseModel):
    id: int
    name: str
