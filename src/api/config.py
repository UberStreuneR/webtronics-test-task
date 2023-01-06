from pydantic import BaseSettings, PostgresDsn
from functools import lru_cache


class Settings(BaseSettings):
    database_url: PostgresDsn
    SECRET_KEY: str
    access_token_expires_minutes: int


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
