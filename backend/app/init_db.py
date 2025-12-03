# backend/app/init_db.py

from __future__ import annotations

import csv
from pathlib import Path

from sqlalchemy.orm import Session

from backend.app.database import SessionLocal, engine
from backend.app.models import Base, User, Club  # ВАЖНО: тези класове вече ги имаш в models.py
from backend.app.security import get_password_hash


def _ensure_user(
    db: Session,
    email: str,
    name: str,
    role: str,
    password: str,
) -> None:
    """
    Създава потребител, само ако го няма вече.
    """
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return

    user = User(
        email=email,
        name=name,
        role=role,
        password_hash=get_password_hash(password),
    )
    db.add(user)
    db.commit()


def _seed_users(db: Session) -> None:
    """
    Създава началните акаунти:
    - platform_admin
    - bfv_admin
    """
    _ensure_user(
        db,
        email="admin@volley.bg",
        name="Platform Admin",
        role="platform_admin",  # според API примера за /auth/me
        password="admin123",
    )

    _ensure_user(
        db,
        email="bfv@volley.bg",
        name="BFV Moderator",
        role="bfv_admin",
        password="bfv123",
    )


def _seed_clubs(db: Session) -> None:
    """
    По желание: чете backend/app/data/clubs.csv и добавя клубове, които ги няма.

    Очаквани колони (заглавия на колоните в CSV):
    - name
    - city  (по желание)
    - logo_url (по желание)
    - contact_email (по желание)
    - contact_phone (по желание)
    """
    csv_path = Path(__file__).parent / "data" / "clubs.csv"

    if not csv_path.exists():
        # Нищо не правим, ако няма файл – това НЕ е грешка
        return

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = (row.get("name") or "").strip()
            if not name:
                continue

            existing = db.query(Club).filter(Club.name == name).first()
            if existing:
                continue

            club = Club(
                name=name,
                city=(row.get("city") or "").strip() or None,
                logo_url=(row.get("logo_url") or "").strip() or None,
                contact_email=(row.get("contact_email") or "").strip() or None,
                contact_phone=(row.get("contact_phone") or "").strip() or None,
            )
            db.add(club)

        db.commit()


def init_db() -> None:
    """
    Основна функция:
    - създава всички таблици от SQLAlchemy моделите
    - добавя начални потребители
    - по желание добавя клубове от CSV
    """
    # 1) Създаваме таблиците (ако вече съществуват, нищо лошо – create_all е идемпотентно)
    Base.metadata.create_all(bind=engine)

    # 2) Seed-ване на данни
    db = SessionLocal()
    try:
        _seed_users(db)
        _seed_clubs(db)
    finally:
        db.close()


# Позволява локално пускане: python -m backend.app.init_db
if __name__ == "__main__":
    init_db()
