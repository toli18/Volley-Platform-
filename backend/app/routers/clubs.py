from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.dependencies import get_db_session, require_role
from backend.app.models import Club, User, UserRole
from backend.app.schemas import ClubSchema, UserReadSchema
from backend.app.security import get_password_hash

router = APIRouter(prefix="/clubs", tags=["clubs"])


@router.get("/", response_model=list[ClubSchema])
def list_clubs(db: Session = Depends(get_db_session)):
    return db.query(Club).all()


@router.post(
    "/",
    response_model=ClubSchema,
    dependencies=[Depends(require_role(UserRole.platform_admin))],
)
def create_club(club: dict, db: Session = Depends(get_db_session)):
    name = club.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="name is required")
    existing = db.query(Club).filter(Club.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Club already exists")
    obj = Club(name=name, city=club.get("city"), logo_url=club.get("logo_url"))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.post(
    "/{club_id}/coaches", dependencies=[Depends(require_role(UserRole.bfv_admin))]
)
def add_coach(
    club_id: int, payload: dict, db: Session = Depends(get_db_session)
) -> UserReadSchema:
    email = payload.get("email")
    name = payload.get("name")
    password = payload.get("password", "changeme123")
    if not email or not name:
        raise HTTPException(status_code=400, detail="email and name required")
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(
        email=email,
        name=name,
        role=UserRole.coach,
        password_hash=get_password_hash(password),
        club_id=club.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
