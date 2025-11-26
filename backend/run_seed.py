from backend.app.seed.seed_all_clubs import seed_all_clubs
from backend.app.seed.seed_clubs_and_coaches import seed_clubs_and_coaches
from backend.app.database import SessionLocal


def main() -> None:
    db = SessionLocal()
    try:
        seed_all_clubs(db)
        seed_clubs_and_coaches(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
