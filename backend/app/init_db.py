import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError

from backend.app.auth import get_password_hash
from backend.app.database import Base, SessionLocal, engine
from backend.app.models import User, UserRole
from backend.app.seed.seed_clubs import seed_clubs
from backend.app.seed.seed_drills import seed_drills
from backend.app.settings import settings


def run_alembic():
    """Apply migrations safely on Render (skip if tables already exist)."""
    alembic_cfg = Config(str(settings.alembic_ini_path))

    alembic_cfg.set_main_option("script_location", str(settings.migrations_path))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)

    try:
        command.upgrade(alembic_cfg, "head")
        print("✅ Alembic migrations applied.")

    except Exception as exc:
        message = str(exc).lower()

        # Skip duplicate table / column errors on Render
        skip_errors = [
            "already exists",
            "duplicate",
            "relation",
        ]

        if any(err in message for err in skip_errors):
            print("⚠️ Skipping migration errors (tables already exist).")
            return

        print("❌ Alembic migration error:", exc)
        raise


def seed_platform_admin() -> None:
    """Create default platform admin if not exists."""
    session = SessionLocal()

    try:
        existing_admin = session.execute(
            select(User).where(User.role == UserRole.platform_admin)
        ).scalar_one_or_none()

        if existing_admin:
            print("ℹ️ Platform admin already exists, skipping.")
            return

        email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        password = os.getenv("ADMIN_PASSWORD", "changeme123")

        admin_user = User(
            email=email,
            password_hash=get_password_hash(password),
            name="Platform Admin",
            role=UserRole.platform_admin,
            club_id=None,
        )

        session.add(admin_user)
        session.commit()
        print(f"✅ Created platform admin user ({email}).")

    except SQLAlchemyError as exc:
        session.rollback()
        print("❌ Failed to seed admin user:", exc)

    finally:
        session.close()


def init_db() -> None:
    """Initialize DB, run migrations, seed data."""
    try:
        # Safety net — ensure tables exist before Alembic runs
        Base.metadata.create_all(bind=engine)

        # Run migrations (safe mode)
        run_alembic()

        # Seed admin + static CSV data
        seed_platform_admin()
        seed_clubs()
        seed_drills()

        print("✅ Database initialization complete.")

    except Exception as exc:
        print("❌ DB initialization failed:", exc)
        raise
