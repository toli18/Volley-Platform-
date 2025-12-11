import csv
from pathlib import Path
from typing import List

from sqlalchemy import select
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from backend.app.database import SessionLocal
from backend.app.models import Drill

CSV_PATH = Path(__file__).resolve().parent / "volleyball_full_transformed.csv"


def parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def seed_drills() -> None:
    if not CSV_PATH.exists():
        print("⚠️ drills CSV not found, skipping seeding.")
        return

    session = SessionLocal()

    try:
        try:
            existing_ids = {drill_id for (drill_id,) in session.execute(select(Drill.id)).all()}
        except OperationalError:
            print("⚠️ Drill table not ready yet, skipping seeding.")
            return

        new_drills: List[Drill] = []

        with CSV_PATH.open(newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                if not any((value or "").strip() for value in row.values()):
                    continue

                drill_id = parse_int(row.get("id"))
                if drill_id is None or drill_id in existing_ids:
                    continue

                drill = Drill(
                    id=drill_id,
                    name=row.get("name"),
                    category=row.get("category"),
                    level=row.get("level"),
                    skill_focus=row.get("skillFocus"),
                    goal=row.get("goal"),
                    description=row.get("description"),
                    variations=row.get("variations"),
                    players=row.get("players"),
                    equipment=row.get("equipment"),
                    rpe=row.get("rpe"),
                    duration_min=parse_int(row.get("durationMin")),
                    duration_max=parse_int(row.get("durationMax")),
                    image_urls=row.get("imageUrls"),
                    video_urls=row.get("videoUrls"),
                    skill_domains=row.get("skill_domains"),
                    game_phases=row.get("game_phases"),
                    tactical_focus=row.get("tactical_focus"),
                    technical_focus=row.get("technical_focus"),
                    position_focus=row.get("position_focus"),
                    zone_focus=row.get("zone_focus"),
                    complexity_level=parse_int(row.get("complexity_level")),
                    decision_level=parse_int(row.get("decision_level")),
                    age_min=parse_int(row.get("age_min")),
                    age_max=parse_int(row.get("age_max")),
                    intensity_type=row.get("intensity_type"),
                    training_goal=row.get("training_goal"),
                    type_of_drill=row.get("type_of_drill"),
                )

                existing_ids.add(drill_id)
                new_drills.append(drill)

        if new_drills:
            session.add_all(new_drills)
            session.commit()
            print(f"✅ Seeded {len(new_drills)} drills.")
        else:
            print("ℹ️ Drills already seeded.")

    except SQLAlchemyError as exc:
        session.rollback()
        print("❌ Failed to seed drills:", exc)
    finally:
        session.close()
