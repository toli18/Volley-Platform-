from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Volley Platform API"
    debug: bool = False

    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/volley_platform"
    )

    # Alembic paths
    alembic_ini_path: Path = Path(__file__).resolve().parent.parent / "alembic.ini"
    migrations_path: Path = Path(__file__).resolve().parent / "migrations"

    jwt_secret: str = Field(default="changeme-secret")
    jwt_algorithm: str = "HS256"
    access_token_expires_minutes: int = 60
    refresh_token_expires_minutes: int = 60 * 24 * 7

    storage_path: str = "./storage"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
