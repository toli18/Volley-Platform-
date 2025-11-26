from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.dependencies import get_db_session, require_role
from backend.app.models import Club, User, UserRole
from backend.app.schemas import (
    ClubCreate,
    ClubDetail,
    ClubRead,
    ClubUpdate,
    CoachCreate,
    CoachRead,
    CoachUpdate,
)
from backend.app.security import get_password_hash

router = APIRouter(prefix="/clubs", tags=["clubs"])


@router.get("/", response_model=list[ClubRead])
def list_clubs(db: Session = Depends(get_db_session)):
    return db.query(Club).all()


@router.get("/{club_id}", response_model=ClubDetail)
def get_club(club_id: int, db: Session = Depends(get_db_session)):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    return club


@router.post(
    "/",
    response_model=ClubRead,
    dependencies=[Depends(require_role(UserRole.platform_admin, UserRole.bfv_admin))],
)
def create_club(club: ClubCreate, db: Session = Depends(get_db_session)):
    existing = db.query(Club).filter(Club.name == club.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Club already exists")
    obj = Club(name=club.name, city=club.city, logo_url=club.logo_url)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch(
    "/{club_id}",
    response_model=ClubRead,
    dependencies=[Depends(require_role(UserRole.platform_admin, UserRole.bfv_admin))],
)
def update_club(
    club_id: int, club_update: ClubUpdate, db: Session = Depends(get_db_session)
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    update_data = club_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(club, field, value)

    db.commit()
    db.refresh(club)
    return club


@router.delete(
    "/{club_id}",
    dependencies=[Depends(require_role(UserRole.platform_admin, UserRole.bfv_admin))],
)
def delete_club(club_id: int, db: Session = Depends(get_db_session)):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    db.delete(club)
    db.commit()
    return {"detail": "Club deleted"}


@router.get(
    "/{club_id}/coaches",
    response_model=list[CoachRead],
)
def list_club_coaches(club_id: int, db: Session = Depends(get_db_session)):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    return (
        db.query(User)
        .filter(User.club_id == club_id, User.role == UserRole.coach)
        .all()
    )


@router.post(
    "/{club_id}/coaches",
    response_model=CoachRead,
    dependencies=[Depends(require_role(UserRole.platform_admin, UserRole.bfv_admin))],
)
def add_coach(
    club_id: int, payload: CoachCreate, db: Session = Depends(get_db_session)
) -> CoachRead:
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    password = payload.password or "123456"
    user = User(
        email=payload.email,
        name=payload.name,
        role=UserRole.coach,
        password_hash=get_password_hash(password),
        club_id=club.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.patch(
    "/{club_id}/coaches/{coach_id}",
    response_model=CoachRead,
    dependencies=[Depends(require_role(UserRole.platform_admin, UserRole.bfv_admin))],
)
def update_coach(
    club_id: int,
    coach_id: int,
    payload: CoachUpdate,
    db: Session = Depends(get_db_session),
) -> CoachRead:
    coach = (
        db.query(User)
        .filter(
            User.id == coach_id, User.club_id == club_id, User.role == UserRole.coach
        )
        .first()
    )
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")

    if payload.email:
        existing = (
            db.query(User)
            .filter(User.email == payload.email, User.id != coach_id)
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")

    update_data = payload.model_dump(exclude_unset=True)
    password = update_data.pop("password", None)
    for field, value in update_data.items():
        setattr(coach, field, value)
    if password:
        coach.password_hash = get_password_hash(password)

    db.commit()
    db.refresh(coach)
    return coach


@router.delete(
    "/{club_id}/coaches/{coach_id}",
    dependencies=[Depends(require_role(UserRole.platform_admin, UserRole.bfv_admin))],
)
def delete_coach(club_id: int, coach_id: int, db: Session = Depends(get_db_session)):
    coach = (
        db.query(User)
        .filter(
            User.id == coach_id, User.club_id == club_id, User.role == UserRole.coach
        )
        .first()
    )
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    db.delete(coach)
    db.commit()
    return {"detail": "Coach deleted"}
