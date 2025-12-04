import csv
from pathlib import Path
from typing import Dict, List

from alembic import command
from alembic.config import Config
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from .database import Base, SessionLocal, engine
from .models import Club
from .settings import settings

SEED_DIR = Path(__file__).parent / "seed"


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


def _load_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader if any((value or "").strip() for value in row.values())]


def seed_clubs() -> None:
    csv_path = SEED_DIR / "clubs.csv"
    rows = _load_csv(csv_path)
    if not rows:
        return

    session = SessionLocal()
    try:
        existing_names = {name for (name,) in session.execute(select(Club.name)).all()}
        new_clubs: List[Club] = []

        for row in rows:
            name = (row.get("name") or "").strip()
            if not name or name in existing_names:
                continue

            club = Club(
                name=name,
                city=(row.get("city") or None),
                country=(row.get("country") or None),
                address=(row.get("address") or None),
                contact_email=(row.get("contact_email") or None),
                contact_phone=(row.get("contact_phone") or None),
                website_url=(row.get("website_url") or None),
                logo_url=(row.get("logo_url") or None),
            )
            existing_names.add(name)
            new_clubs.append(club)

        if new_clubs:
            session.add_all(new_clubs)
            session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()
