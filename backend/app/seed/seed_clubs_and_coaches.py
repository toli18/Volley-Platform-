from sqlalchemy.orm import Session

from backend.app import models
from backend.app.database import SessionLocal
from backend.app.security import get_password_hash

CLUBS = [
    "Троян Волей",
    "Вотев Враца",
    "Олимпиец Плевен",
    "Славена Никован",
    "Владимир Картаров",
    "Петър Игнатов",
    "Анатоли Пенев",
    "Дариа Георгиева",
]


def run():
    db: Session = SessionLocal()

    for club_name in CLUBS:
        existing_club = (
            db.query(models.Club).filter(models.Club.name == club_name).first()
        )
        if existing_club:
            club = existing_club
        else:
            club = models.Club(name=club_name)
            db.add(club)
            db.commit()
            db.refresh(club)

        # Create 2 coaches per club
        for i in range(1, 3):
            email = f"{club_name.lower().replace(' ', '_')}_coach{i}@test.bg"

            exists = db.query(models.User).filter(models.User.email == email).first()
            if exists:
                continue

            coach = models.User(
                email=email,
                name=f"Треньор {i} - {club_name}",
                role=models.UserRole.coach,
                club_id=club.id,
                hashed_password=get_password_hash("123456"),
            )
            db.add(coach)

        db.commit()


if __name__ == "__main__":
    run()
