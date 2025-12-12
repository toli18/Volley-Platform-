from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.settings import settings

# SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """
    Dependency used in FastAPI routes.
    Creates a new DB session for the request and closes it afterward.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
