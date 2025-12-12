from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import Drill

router = APIRouter()


@router.get("/", summary="List all drills")
def list_drills(db: Session = Depends(get_db)):
    return db.query(Drill).all()
