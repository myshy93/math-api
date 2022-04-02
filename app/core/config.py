import secrets

from pydantic import BaseSettings

default_user = {
    "email": "test@test.com",
    "password": "test",
    "name": "Test"
}

LOGGER_NAME = "global"


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    PROJECT_NAME: str = "Math Microservice"
    DATABASE_URL: str = "sqlite:///./math.db"
    DEBUG: bool = False
    SERVER_URL: str = 'localhost'

    class Config:
        case_sensitive = True


settings = Settings()
