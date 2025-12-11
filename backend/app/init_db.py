import os

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


def run_migrations() -> None:
    """Apply migrations and seed data if necessary."""
    alembic_cfg = Config(str(settings.alembic_ini_path))
    alembic_cfg.set_main_option("script_location", str(settings.migrations_path))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    command.upgrade(alembic_cfg, "head")


def seed_platform_admin() -> None:
    session = SessionLocal()

    try:
        existing_admin = session.execute(
            select(User).where(User.role == UserRole.PLATFORM_ADMIN)
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
            role=UserRole.PLATFORM_ADMIN,
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


def init_db() -> None:
    """Initialize database tables and seed initial data."""

    try:
        run_migrations()
    except OperationalError as e:
        print("Database connection failed:", e)
        return False
    except Exception as e:  # pragma: no cover - defensive catch for startup
        print("Unexpected error while running migrations:", e)
        return False

    seed_clubs()
    seed_drills()
    seed_platform_admin()
    return True

