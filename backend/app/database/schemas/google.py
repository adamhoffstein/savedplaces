from pydantic import BaseModel


class Nearby(BaseModel):
    username: str
    full_name: str
