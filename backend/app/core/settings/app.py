from app.core.settings.base import BaseAppSettings
from pydantic import Field


class AppSettings(BaseAppSettings):
    google_places_key: str = Field(str, env="GOOGLE_PLACES_KEY")
    db_user: str = Field(str, env="DB_USER")
    db_pass: str = Field(str, env="DB_PASS")
    db_host: str = Field(str, env="DB_HOST")
    db_name: str = Field(str, env="DB_NAME")
    secret_key: str = Field(str, env="SECRET_KEY")
    algorithm: str = Field(str, env="ALGORITHM")
    access_token_expire_minutes: int = Field(
        str, env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    refresh_token_expire_minutes: int = Field(
        str, env="REFRESH_TOKEN_EXPIRE_MINUTES"
    )
