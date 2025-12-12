from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import Club

router = APIRouter()


@router.get("/", summary="List all clubs")
def list_clubs(db: Session = Depends(get_db)):
    return db.query(Club).all()
