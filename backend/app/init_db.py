from pathlib import Path

from alembic import command
from alembic.config import Config

from backend.app.seed.seed_clubs import seed_clubs
from .database import Base, engine
from .settings import settings


def init_db() -> None:
    """Apply migrations and seed data if necessary."""
    run_migrations()
    Base.metadata.create_all(bind=engine)
    seed_clubs()


def run_migrations() -> None:
    alembic_cfg = Config(str(settings.alembic_ini_path))
    migrations_path = Path(__file__).resolve().parent / "migrations"
    alembic_cfg.set_main_option("script_location", str(migrations_path))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    command.upgrade(alembic_cfg, "head")
