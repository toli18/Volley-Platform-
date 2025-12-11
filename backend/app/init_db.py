import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import select
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from backend.app.auth import get_password_hash
from backend.app.database import SessionLocal
from backend.app.models import User, UserRole
from backend.app.seed import seed_clubs
from backend.app.seed.seed_drills import seed_drills
from backend.app.settings import settings


def _build_alembic_config() -> Config:
    ini_path: Path = settings.alembic_ini_path
    if not ini_path.exists():
        raise FileNotFoundError(f"Alembic config not found at {ini_path}")

    alembic_cfg = Config(str(ini_path))
    alembic_cfg.set_main_option("script_location", str(settings.migrations_path))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    return alembic_cfg


def run_migrations() -> None:
    """Apply migrations. Fail fast if something goes wrong."""

    alembic_cfg = _build_alembic_config()
    command.upgrade(alembic_cfg, "head")


def seed_platform_admin() -> None:
    session = SessionLocal()

    try:
        existing_admin = session.execute(
            select(User).where(User.role == UserRole.platform_admin)
        ).scalar_one_or_none()

        if existing_admin:
            print("ℹ️ Platform admin already exists.")
            return

        email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        password = os.getenv("ADMIN_PASSWORD", "changeme123")

        existing_by_email = session.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()
        if existing_by_email:
            print("ℹ️ Admin email already used, skipping creation.")
            return

        admin_user = User(
            email=email,
            password_hash=get_password_hash(password),
            name="Platform Admin",
            role=UserRole.platform_admin,
            club_id=None,
        )

        session.add(admin_user)
        session.commit()
        print(f"✅ Created platform admin user {email}.")
    except SQLAlchemyError as exc:
        session.rollback()
        print("❌ Failed to seed admin user:", exc)
    finally:
        session.close()


def init_db() -> bool:
    """Run migrations, then idempotent seeders."""

    try:
        run_migrations()
    except OperationalError as e:
        print("Database connection failed:", e)
        raise
    except Exception as e:  # pragma: no cover - defensive catch for startup
        print("Unexpected error while running migrations:", e)
        raise

    seed_clubs()
    seed_drills()
    seed_platform_admin()
    return True
