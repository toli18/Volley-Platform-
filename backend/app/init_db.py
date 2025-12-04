from sqlalchemy.orm import Session
from backend.app.database import Base, engine, SessionLocal
from backend.app.seed.clubs import seed_clubs

def init_db():
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        seed_clubs(db)
    finally:
        db.close()

