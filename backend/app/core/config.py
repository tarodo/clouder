import secrets

from environs import Env
from pydantic import BaseSettings

env = Env()
env.read_env()


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALLOWED_ORIGINS: list = ["http://127.0.0.1:3000", "http://localhost:3000", "https://www.beatport.com/"]
    ALGORITHM: str = "HS256"
    DB_URL: str = "sqlite:///db_test.db"

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    EMAIL_TEST_USER: str = "test@test.com"

    class Config:
        case_sensitive = True


settings = Settings()
