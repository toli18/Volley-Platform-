import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import select
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from backend.app.auth import get_password_hash
from backend.app.database import Base, SessionLocal, engine
from backend.app.models import User, UserRole
from backend.app.seed.seed_clubs import seed_clubs
from backend.app.seed.seed_drills import seed_drills
from backend.app.settings import settings


def run_alembic() -> None:
    """Run migrations and seed data if necessary."""
    ini_path = Path(settings.alembic_ini_path)

    if not ini_path.exists():
        raise FileNotFoundError(f"Alembic config not found at {ini_path}")

    alembic_cfg = Config(str(ini_path))
    alembic_cfg.set_main_option("script_location", settings.migrations_path)
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)

    # Apply migrations
    command.upgrade(alembic_cfg, "head")


def seed_platform_admin() -> None:
    """Create default platform admin if not exists."""
    session = SessionLocal()

    try:
        existing_admin = session.execute(
            select(User).where(User.role == UserRole.platform_admin)
        ).scalar_one_or_none()

        if existing_admin:
            print("ℹ️ Platform admin already exists, skipping.")
            session.close()
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
    """Initialize database tables and seed initial data."""
    try:
        # Ensure tables exist before migrations (safety net)
        Base.metadata.create_all(bind=engine)

        # Run migrations
        run_alembic()

        # Seed platform admin
        seed_platform_admin()

        # Seed CSV-driven data
        seed_clubs()
        seed_drills()

    except Exception as exc:
        print("❌ DB initialization failed:", exc)
        raise
