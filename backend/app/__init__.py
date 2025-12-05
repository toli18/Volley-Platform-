from sqlalchemy.exc import OperationalError
from backend.app.database import Base, engine
from backend.app.seed.database import seed_clubs


def init_db() -> None:
    """
    Initialize database tables and seed initial data.
    """

    # Create tables
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError as e:
        print("Database connection failed:", e)
        return

    # Seed initial data (only if missing)
    seed_clubs()
