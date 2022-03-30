from app.core.settings.base import BaseAppSettings
from pydantic import Field


class AppSettings(BaseAppSettings):
    google_places_key: str = Field(str, env="GOOGLE_PLACES_KEY")
    db_user: str = Field(str, env="DB_USER")
    db_pass: str = Field(str, env="DB_PASS")
    db_host: str = Field(str, env="DB_HOST")
    db_name: str = Field(str, env="DB_NAME")
