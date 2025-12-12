from alembic import command
from alembic.config import Config

from backend.app.settings import settings
from backend.app.seed.seed_clubs import seed_clubs
from backend.app.seed.seed_drills import seed_drills
from backend.app.models import User, UserRole
from backend.app.database import SessionLocal
from backend.app.auth import get_password_hash


def run_alembic():
    alembic_cfg = Config(str(settings.alembic_ini_path))
    alembic_cfg.set_main_option("script_location", str(settings.migrations_path))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)

    command.upgrade(alembic_cfg, "head")
    print("✅ Alembic migrations applied.")


def init_db() -> None:
    try:
        run_alembic()
        seed_platform_admin()
        seed_clubs()
        seed_drills()
        print("✅ Database initialization complete.")
    except Exception as exc:
        print("❌ DB initialization failed:", exc)
        raise
