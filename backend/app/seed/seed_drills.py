import csv
from backend.app.database import SessionLocal
from backend.app.models import Drill

CSV_PATH = "backend/app/seed/volleyball_full_transformed.csv"

def seed_drills():
    db = SessionLocal()

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            drill = Drill(
                id=int(row["id"]),
                name=row["name"],
                category=row["category"],
                level=row["level"],
                skill_focus=row["skillFocus"],
                goal=row["goal"],
                description=row["description"],
                variations=row["variations"],
                players=row["players"],
                equipment=row["equipment"],
                rpe=row["rpe"],
                duration_min=parse_int(row["durationMin"]),
                duration_max=parse_int(row["durationMax"]),
                image_urls=row["imageUrls"],
                video_urls=row["videoUrls"],
                skill_domains=row["skill_domains"],
                game_phases=row["game_phases"],
                tactical_focus=row["tactical_focus"],
                technical_focus=row["technical_focus"],
                position_focus=row["position_focus"],
                zone_focus=row["zone_focus"],
                complexity_level=parse_int(row["complexity_level"]),
                decision_level=parse_int(row["decision_level"]),
                age_min=parse_int(row["age_min"]),
                age_max=parse_int(row["age_max"]),
                intensity_type=row["intensity_type"],
                training_goal=row["training_goal"],
                type_of_drill=row["type_of_drill"],
            )

            db.add(drill)

        db.commit()
        db.close()


def parse_int(value):
    try:
        return int(value)
    except:
        return None
