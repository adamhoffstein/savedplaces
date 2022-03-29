import logging

from pydantic import Field

from app.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    debug: bool = True

    title: str = "Test FastAPI example application"

    logging_level: int = logging.DEBUG

    test_admin_user: str = Field(str, env="TEST_ACCOUNT_ID")
    test_admin_password: str = Field(str, env="TEST_ACCOUNT_PW")

    class Config(AppSettings.Config):
        env_file = ".env"
