from backend.app.seed.seed_clubs import seed_clubs
from backend.app.seed.seed_drills import seed_drills
from backend.app.models import User, UserRole
from backend.app.database import SessionLocal
from backend.app.auth import get_password_hash
import os
from sqlalchemy import select


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

        admin = User(
            email=email,
            password_hash=get_password_hash(password),
            name="Platform Admin",
            role=UserRole.platform_admin,
        )

        session.add(admin)
        session.commit()
        print("✅ Platform admin created.")

    finally:
        session.close()


def init_db() -> None:
    seed_platform_admin()
    seed_clubs()
    seed_drills()
    print("✅ Seed completed.")
