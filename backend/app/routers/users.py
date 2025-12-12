from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import User

router = APIRouter()


@router.get("/", summary="List all users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
