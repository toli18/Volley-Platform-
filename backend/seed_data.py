from pathlib import Path
from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from backend.app.config import settings
from backend.app.models import Base, User, UserRole, Club, Exercise, Article
from backend.app.security import get_password_hash


def ensure_database():
    engine = create_engine(settings.database_url, future=True)
    Base.metadata.create_all(engine)
    return engine


def create_user(db: Session, email: str, name: str, role: UserRole, club_id=None, password="changeme123") -> User:
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return existing
    user = User(email=email, name=name, role=role, club_id=club_id, password_hash=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def load_exercises_from_excel(db: Session, path: Path, created_by: int | None = None):
    if not path.exists():
        print(f"Excel file not found at {path}, skipping import")
        return
    df = pd.read_excel(path)
    for _, row in df.iterrows():
        name = row.get("name") or row.get("Name")
        if not name:
            continue
        exercise = Exercise(
            name=name,
            main_category=row.get("main_category") or row.get("category") or "general",
            sub_category=row.get("sub_category"),
            level=row.get("level"),
            goal=row.get("goal"),
            description=row.get("description"),
            players_required=row.get("players_required") if not pd.isna(row.get("players_required")) else None,
            intensity=row.get("intensity"),
            duration_min=row.get("duration_min") if not pd.isna(row.get("duration_min")) else None,
            duration_max=row.get("duration_max") if not pd.isna(row.get("duration_max")) else None,
            tags=row.get("tags") if isinstance(row.get("tags"), list) else [],
            age_groups=row.get("age_groups") if isinstance(row.get("age_groups"), list) else [],
            created_by=created_by,
        )
        db.add(exercise)
    db.commit()


def seed():
    engine = ensure_database()
    with Session(engine) as db:
        admin = create_user(db, "admin@system.bg", "Platform Admin", UserRole.platform_admin, password="admin123")
        bfv_admin = create_user(db, "bfv_admin@bvf.bg", "BFV Admin", UserRole.bfv_admin, password="bfv123")

        clubs = [
            ("Троян Волей", "Троян"),
            ("Вотев Враца", "Враца"),
            ("Олимпиец Плевен", "Плевен"),
            ("Дариа Спорт", ""),
        ]
        club_entities: List[Club] = []
        for name, city in clubs:
            existing = db.query(Club).filter(Club.name == name).first()
            if existing:
                club_entities.append(existing)
                continue
            club = Club(name=name, city=city)
            db.add(club)
            db.commit()
            db.refresh(club)
            club_entities.append(club)

        trojan = next(c for c in club_entities if c.name == "Троян Волей")
        create_user(db, "coach1@test.bg", "Анатоли Пенев", UserRole.coach, club_id=trojan.id, password="coach123")
        create_user(db, "coach2@test.bg", "Петър Игнатов", UserRole.coach, club_id=trojan.id, password="coach123")
        create_user(db, "coach3@test.bg", "Владимир Картаров", UserRole.coach, club_id=trojan.id, password="coach123")
        create_user(db, "coach4@test.bg", "Славена Никова", UserRole.coach, club_id=trojan.id, password="coach123")

        create_user(db, "votsev.vratza@test.bg", "Вотев Враца Коуч", UserRole.coach, club_id=next(c for c in club_entities if c.name == "Вотев Враца").id, password="coach123")
        create_user(db, "olympiec.pleven@test.bg", "Олимпиец Плевен", UserRole.coach, club_id=next(c for c in club_entities if c.name == "Олимпиец Плевен").id, password="coach123")
        create_user(db, "coach5@test.bg", "Дариа Георгиева", UserRole.coach, club_id=next(c for c in club_entities if c.name == "Дариа Спорт").id, password="coach123")

        sample_article = db.query(Article).first()
        if not sample_article:
            article = Article(title="Примерна статия", content="Тестов материал", created_by=admin.id, status="published", approved_by=admin.id)
            db.add(article)
            db.commit()

        excel_path = Path("/mnt/data/volleyball_exercises_normalized.xlsx")
        load_exercises_from_excel(db, excel_path, created_by=bfv_admin.id)

    print("Seed completed")


if __name__ == "__main__":
    seed()
