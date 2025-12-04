from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration."""

    database_url: str = "postgresql+psycopg://user:password@localhost:5432/postgres"
    alembic_ini_path: Path = Path(__file__).resolve().parents[2] / "alembic.ini"

    class Config:
        env_file = ".env"
        env_prefix = ""
        extra = "ignore"


settings = Settings()
