from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Volley Platform API"
    debug: bool = False

    # ⚠️ НЯМА default → ENV DATABASE_URL се зарежда правилно
    database_url: str = Field(...)

    jwt_secret: str = Field(default="changeme-secret")
    jwt_algorithm: str = "HS256"
    access_token_expires_minutes: int = 60
    refresh_token_expires_minutes: int = 60 * 24 * 7
    storage_path: str = "./storage"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
