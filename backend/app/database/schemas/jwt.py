from typing import Optional, List
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    super_admin: Optional[bool]


class TokenData(BaseModel):
    username: Optional[str] = None
