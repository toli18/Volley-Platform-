from pathlib import Path
import re
from typing import List

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.models import Article, Base, Club, Exercise, User, UserRole
from backend.app.security import get_password_hash


# Comprehensive club list across regions
CLUB_NAMES = [
    "ЦПВК",
    "ВК Локомотив 1929 Нидо",
    "ВК Софийски университет",
    "СКВ Звезди 94",
    "ВК ЦСКА",
    "УВК Хектор",
    "ВК Септември ПроСинема",
    "СК ВАСК",
    "ВК Люлин",
    "КВ при ОСК Славия",
    "СК Славия 2017",
    "СК Барутов волей",
    "ВК Ахил",
    "ВК Левски София",
    "ВК Академик Волей",
    "ВК Владимир Николов",
    "ВК Армеец",
    "ВК Симеонови супер волей",
    "ВК Хебър – Пазарджик",
    "СК Левски 2005 – Карлово",
    "СКВ Родопа – Смолян",
    "ВК Марица – Белово",
    "ВК Велинград Волей",
    "ВК Металик Волей – Сопот",
    "ВК Тополово",
    "ВК Пан – волей – Панагюрище",
    "ВК Марица – Пловдив",
    "ВК Виктория Волей – Пловдив",
    "ПСК Локомотив – Пловдив",
    "ВК Топ Волей – Пещера",
    "ВК Въча – Девин",
    "ВК Асеновград",
    "ВК Локомотив АВИА – Пловдив",
    "ВК Асеновец – Асеновград",
    "ВК Крепост Хисаря",
    "ВК Марица 2022 – Пловдив",
    "ВК Коини Волей – Първомай",
    "СК Ракитово Волей – Костандово",
    "ВК Карлово Волей",
    "ВК Казанлък",
    "ВК Любимец 2010",
    "ВК Яворов – Чирпан",
    "СКВ Тунджа – Ямбол",
    "ВК Раковски – Димитровград",
    "СКВ Сливен Волей",
    "ВК Раднево Волей",
    "ВК Дея спорт – Бургас",
    "ВК Берое 2016 – Стара Загора",
    "ВК Царево",
    "ВК Загорец – Нова Загора",
    "СКВ Берое – Стара Загора",
    "ВК Нефтохимик 2010 – Бургас",
    "СВК Арда – Кърджали",
    "ВК Странджа – Средец",
    "ВК Сливен",
    "ВК Айтос",
    "СК Бургас Волей 2009",
    "ВК Кирково 15",
    "ВК Хеброс – Харманли",
    "СК Гръм в рая – Свиленград",
    "ВК Славейков – Димитровград",
    "ВК Арда 2022 – Кърджали",
    "ВК Бургос волей – Бургас",
    "ВК Бургас – 2007",
    "ВК Ропотомо – Приморско",
    "ВК Хаштаг Бургас",
    "ВК Бийч Волей Бургас",
    "ВК Несебър Волей",
    "ВК Козлодуй – мъже",
    "КВ Раковски – 1964 – Севлиево",
    "ВК Монтана Волей",
    "ВК Севлиево Волей",
    "ВК Царевец 19 – Велико Търново",
    "ВК Ботев – Луковит",
    "ВК Вършец",
    "ВК Бдин – Вида – Видин",
    "СКВ Ботев – Враца",
    "ВК Осъм – Ловеч",
    "ВК Чавдар 1932 – Бяла Слатина",
    "ВК Спартак 1996 – Плевен",
    "СКВ Павликени",
    "ВК Град – Белоградчик",
    "ВК Импулс – Долна Оряховица",
    "ВК Троян волей",
    "ВК Локомотив – Червен бряг",
    "ВК Изгрев – Ябланица",
    "СВК Тетевен Волей",
    "СК Тони спорт – Берковица",
    "СКВ Олимпиец – Плевен",
    "ВК Коко волей 2016 – Новаковци",
    "ВК Бъдин- Волей – Видин",
    "ВК Вел Волей – Велико Търново",
    "ВК Нике – Бяла Слатина",
    "ВК Атом – Козлодуй",
    "СВК Велики Преслав",
    "СКВ Елит – Силистра",
    "СК Вихър – Вълчи дол",
    "СК Перун Варна",
    "СК Йоан Екзарх Български Шумен 05",
    "ВК Хан Аспарух – Исперих",
    "ВК Варна – ДКС",
    "ВК Черноморец Бяла 2008",
    "СК Торо Волей – Варна",
    "ВК Черноломец - Попово 98",
    "ВК Попово 09",
    "ВК Любо Ганев – Автосвят – Русе",
    "ВК Лудогорец – Разград",
    "ВК Омуртаг",
    "ВК Черно море – Варна",
    "СКВ Дунав – Русе",
    "ВК Волов 2020 – Шумен",
    "ВК Родина Суворово",
    "ВК Добруджа 07 – Добрич",
    "СКВ Дием Русе",
    "Русе Волей Клуб",
    "СК Академик Варна",
    "СВК Перун 1 – Варна",
    "СВК Спартак Варна",
    "ВК Бултекс 2013 – Варна",
    "ВК Енерджи – Варна",
    "ВК Сливнишки герой – Сливница",
    "ВК Марек Дупница",
    "ВК Самоков 2009",
    "ВК Медиус Волей – Сандански",
    "ВК Етрополе",
    "ВК Миньор – Перник",
    "ВК Пирин Разлог",
    "ВК Благоевград",
    "ВК Ботев – Ихтиман",
    "СК Волейбол – Пирдоп",
    "ВК Звездец – Горна Малина",
    "ВК Велбъжд – Олимпия – Кюстендил",
    "ВК Ерма 96 – Трън",
    "ВК Металург волей – Перник",
    "ВК Драгоман",
    "ВК Феникс 2024 – Елин Пелин",
]


def slugify_name(value: str) -> str:
    base = (
        value.lower()
        .replace("–", " ")
        .replace("—", " ")
        .replace("„", "")
        .replace("“", "")
    )
    ascii_slug = re.sub(
        r"[^a-z0-9]+", "-", base.encode("ascii", "ignore").decode()
    ).strip("-")
    if not ascii_slug:
        ascii_slug = re.sub(r"\s+", "-", base).strip("-") or "club"
    return ascii_slug


def ensure_database():
    engine = create_engine(settings.database_url, future=True)
    Base.metadata.create_all(engine)
    return engine


def create_user(
    db: Session,
    email: str,
    name: str,
    role: UserRole,
    club_id=None,
    password="changeme123",
) -> User:
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return existing
    user = User(
        email=email,
        name=name,
        role=role,
        club_id=club_id,
        password_hash=get_password_hash(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def seed_all_clubs_and_coaches(db: Session):
    clubs_by_name: dict[str, Club] = {}

    for name in CLUB_NAMES:
        existing = db.query(Club).filter(Club.name == name).first()
        if existing:
            clubs_by_name[name] = existing
            continue

        club_kwargs = {"name": name}
        if hasattr(Club, "status"):
            club_kwargs["status"] = "active"

        club = Club(**club_kwargs)
        db.add(club)
        db.flush()
        clubs_by_name[name] = club

    for club in clubs_by_name.values():
        for idx in range(1, 3):
            email = f"{slugify_name(club.name)}-coach{idx}@coach.test"
            exists = db.query(User).filter(User.email == email).first()
            if exists:
                continue

            coach = User(
                email=email,
                name=f"{club.name} Coach {idx}",
                role=UserRole.coach,
                club_id=club.id,
                password_hash=get_password_hash("123456"),
            )
            db.add(coach)

    db.commit()


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
            players_required=(
                row.get("players_required")
                if not pd.isna(row.get("players_required"))
                else None
            ),
            intensity=row.get("intensity"),
            duration_min=(
                row.get("duration_min")
                if not pd.isna(row.get("duration_min"))
                else None
            ),
            duration_max=(
                row.get("duration_max")
                if not pd.isna(row.get("duration_max"))
                else None
            ),
            tags=row.get("tags") if isinstance(row.get("tags"), list) else [],
            age_groups=(
                row.get("age_groups") if isinstance(row.get("age_groups"), list) else []
            ),
            created_by=created_by,
        )
        db.add(exercise)
    db.commit()


def seed():
    engine = ensure_database()
    with Session(engine) as db:
        admin = create_user(
            db,
            "admin@system.bg",
            "Platform Admin",
            UserRole.platform_admin,
            password="admin123",
        )
        bfv_admin = create_user(
            db, "bfv_admin@bvf.bg", "BFV Admin", UserRole.bfv_admin, password="bfv123"
        )

        seed_all_clubs_and_coaches(db)

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
        create_user(
            db,
            "coach1@test.bg",
            "Анатоли Пенев",
            UserRole.coach,
            club_id=trojan.id,
            password="coach123",
        )
        create_user(
            db,
            "coach2@test.bg",
            "Петър Игнатов",
            UserRole.coach,
            club_id=trojan.id,
            password="coach123",
        )
        create_user(
            db,
            "coach3@test.bg",
            "Владимир Картаров",
            UserRole.coach,
            club_id=trojan.id,
            password="coach123",
        )
        create_user(
            db,
            "coach4@test.bg",
            "Славена Никова",
            UserRole.coach,
            club_id=trojan.id,
            password="coach123",
        )

        create_user(
            db,
            "votsev.vratza@test.bg",
            "Вотев Враца Коуч",
            UserRole.coach,
            club_id=next(c for c in club_entities if c.name == "Вотев Враца").id,
            password="coach123",
        )
        create_user(
            db,
            "olympiec.pleven@test.bg",
            "Олимпиец Плевен",
            UserRole.coach,
            club_id=next(c for c in club_entities if c.name == "Олимпиец Плевен").id,
            password="coach123",
        )
        create_user(
            db,
            "coach5@test.bg",
            "Дариа Георгиева",
            UserRole.coach,
            club_id=next(c for c in club_entities if c.name == "Дариа Спорт").id,
            password="coach123",
        )

        sample_article = db.query(Article).first()
        if not sample_article:
            article = Article(
                title="Примерна статия",
                content="Тестов материал",
                created_by=admin.id,
                status="published",
                approved_by=admin.id,
            )
            db.add(article)
            db.commit()

        excel_path = Path("/mnt/data/volleyball_exercises_normalized.xlsx")
        load_exercises_from_excel(db, excel_path, created_by=bfv_admin.id)

    print("Seed completed")


if __name__ == "__main__":
    seed()
