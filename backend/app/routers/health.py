from fastapi import APIRouter
from backend.app.database import SessionLocal

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
def health():
    return {"status": "ok"}


@router.get("/db")
def db_health():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        return {"database": "ok"}
    except Exception as e:
        return {"database": "error", "details": str(e)}
    finally:
        db.close()
