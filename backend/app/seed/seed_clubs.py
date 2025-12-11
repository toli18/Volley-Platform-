import csv
from pathlib import Path
from typing import Dict, List

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from backend.app.database import SessionLocal
from backend.app.models import Club

SEED_DIR = Path(__file__).resolve().parent


def _load_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        print("⚠️ clubs.csv not found, skipping seeding.")
        return []

    with path.open("r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return [
            row for row in reader
            if any((value or "").strip() for value in row.values())
        ]


def seed_clubs() -> None:
    csv_path = SEED_DIR / "clubs.csv"
    rows = _load_csv(csv_path)

    if not rows:
        print("ℹ️ No clubs to seed.")
        return

    session = SessionLocal()

    try:
        # ✅ SAFE CHECK: if table does NOT exist yet → skip
        try:
            existing_names = {
                name for (name,) in session.execute(select(Club.name)).all()
            }
        except OperationalError:
            print("⚠️ Club table not ready yet, skipping seeding.")
            return

        new_clubs: List[Club] = []

        for row in rows:
            name = (row.get("name") or "").strip()
            if not name or name in existing_names:
                continue

            club = Club(
                name=name,
                city=row.get("city"),
                country=row.get("country"),
                address=row.get("address"),
                contact_email=row.get("contact_email"),
                contact_phone=row.get("contact_phone"),
                website_url=row.get("website_url"),
                logo_url=row.get("logo_url"),
            )

            existing_names.add(name)
            new_clubs.append(club)

        if new_clubs:
            session.add_all(new_clubs)
            session.commit()
            print(f"✅ Seeded {len(new_clubs)} clubs.")
        else:
            print("ℹ️ Clubs already seeded.")

    except SQLAlchemyError as e:
        session.rollback()
        print("❌ Seeding failed:", e)

    finally:
        session.close()
