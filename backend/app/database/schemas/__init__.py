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

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    id: int
    email: EmailStr
    full_name: str


class PlaceBase(BaseModel):
    google_place_id: str
    name: str


class Place(PlaceBase):
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
    updated_date: Optional[datetime]
    created_date: datetime
    assignedplaces: Optional[List[Place]]
    owner: User

    class Config:
        orm_mode = True
