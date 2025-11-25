from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Volley Platform API"
    debug: bool = False
    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/volley_platform"
    )
    jwt_secret: str = Field(default="changeme-secret")
    jwt_algorithm: str = "HS256"
    access_token_expires_minutes: int = 60
    refresh_token_expires_minutes: int = 60 * 24 * 7
    storage_path: str = "./storage"

    
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
