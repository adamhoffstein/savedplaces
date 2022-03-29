from os import environ
from pydantic import BaseSettings


class BaseAppSettings(BaseSettings):
    app_env: str = environ["ENV_STATE"]

    class Config:
        env_file = ".env"
