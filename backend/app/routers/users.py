from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.dependencies.roles import require_role
from backend.app.models import Club, UserRole

router = APIRouter()


@router.post("/")
def create_club(
    club: dict,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.platform_admin)),
):
    db_club = Club(**club)
    db.add(db_club)
    db.commit()
    return db_club
