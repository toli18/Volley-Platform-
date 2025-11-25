import math
from typing import List, Tuple

import pandas as pd
from sqlalchemy.orm import Session

from backend.app import models
from backend.app.database import SessionLocal

EXCEL_PATH = "/mnt/data/volleyball_exercises_normalized.xlsx"


def _clean_value(value):
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return value


def _parse_list(value) -> List[str]:
    if value is None:
        return []
    if isinstance(value, float) and math.isnan(value):
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        parts = [part.strip() for part in value.split(",")]
        return [part for part in parts if part]
    return []


def _to_int(value):
    cleaned = _clean_value(value)
    if cleaned is None:
        return None
    try:
        return int(cleaned)
    except (TypeError, ValueError):
        return None


def import_from_excel(
    path: str = EXCEL_PATH, session: Session | None = None
) -> Tuple[int, int]:
    df = pd.read_excel(path)
    new_count = 0
    updated_count = 0
    owns_session = session is None
    db: Session = session or SessionLocal()

    try:
        for idx, row in df.iterrows():
            name = _clean_value(row.get("name"))
            if not name:
                continue

            main_category = _clean_value(row.get("main_category")) or "general"
            sub_category = _clean_value(row.get("sub_category"))
            level = _clean_value(row.get("level"))
            goal = _clean_value(row.get("goal"))
            description = _clean_value(row.get("description"))
            players_required = _to_int(row.get("players_required"))
            intensity = _clean_value(row.get("intensity"))
            duration_min = _to_int(row.get("duration_min"))
            duration_max = _to_int(row.get("duration_max"))
            tags = _parse_list(row.get("tags"))
            age_groups = _parse_list(row.get("age_groups"))
            image_urls = _parse_list(row.get("image_urls"))
            video_urls = _parse_list(row.get("video_urls"))

            existing = (
                db.query(models.Exercise).filter(models.Exercise.name == name).first()
            )
            if existing:
                existing.main_category = main_category
                existing.sub_category = sub_category
                existing.level = level
                existing.goal = goal
                existing.description = description
                existing.players_required = players_required
                existing.intensity = intensity
                existing.duration_min = duration_min
                existing.duration_max = duration_max
                existing.tags = tags
                existing.age_groups = age_groups
                existing.image_urls = image_urls
                existing.video_urls = video_urls
                updated_count += 1
            else:
                exercise = models.Exercise(
                    name=name,
                    main_category=main_category,
                    sub_category=sub_category,
                    level=level,
                    goal=goal,
                    description=description,
                    players_required=players_required,
                    intensity=intensity,
                    duration_min=duration_min,
                    duration_max=duration_max,
                    tags=tags,
                    age_groups=age_groups,
                    image_urls=image_urls,
                    video_urls=video_urls,
                )
                db.add(exercise)
                new_count += 1

            if (idx + 1) % 50 == 0:
                db.commit()

        db.commit()
    finally:
        if owns_session:
            db.close()

    print(
        f"Imported {new_count} new exercises, updated {updated_count} existing exercises"
    )
    return new_count, updated_count
