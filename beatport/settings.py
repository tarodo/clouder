from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    spotify_service_url: str = ""


bp_settings = Settings()
