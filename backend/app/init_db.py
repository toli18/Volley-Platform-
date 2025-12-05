from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy.exc import OperationalError

from backend.app.database import Base, engine
from backend.app.seed import seed_clubs
from backend.app.settings import settings


def run_migrations() -> None:
    """Apply migrations and seed data if necessary."""
    alembic_cfg = Config(str(settings.alembic_ini_path))
    alembic_cfg.set_main_option("script_location", str(settings.migrations_path))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    command.upgrade(alembic_cfg, "head")


def init_db() -> None:
    """Initialize database tables and seed initial data."""

    try:
        # Apply migrations
        run_migrations()

        # Create tables (fallback)
        Base.metadata.create_all(bind=engine)
    except OperationalError as e:
        print("Database connection failed:", e)
        return

    # Seed initial data
    seed_clubs()

