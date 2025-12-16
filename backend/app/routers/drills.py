from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.dependencies.roles import require_role
from backend.app.models import Drill, UserRole
from backend.app.schemas.drill import DrillCreate, DrillRead

router = APIRouter()


# =========================================================
# GET /drills  – всички роли (public read)
# =========================================================
@router.get("/", response_model=list[DrillRead])
def get_drills(
    level: str | None = None,
    age: int | None = None,
    skill: str | None = None,
    phase: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Drill)

    if level:
        query = query.filter(Drill.level == level)

    if age:
        query = query.filter(
            Drill.age_min <= age,
            Drill.age_max >= age,
        )

    if skill:
        query = query.filter(Drill.skill_domains.ilike(f"%{skill}%"))

    if phase:
        query = query.filter(Drill.game_phases.ilike(f"%{phase}%"))

    return query.all()


# =========================================================
# GET /drills/{id} – всички роли
# =========================================================
@router.get("/{drill_id}", response_model=DrillRead)
def get_drill(
    drill_id: int,
    db: Session = Depends(get_db),
):
    drill = db.query(Drill).filter(Drill.id == drill_id).first()

    if not drill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drill not found",
        )

    return drill


# =========================================================
# POST /drills – само COACH
# =========================================================
@router.post(
    "/",
    response_model=DrillRead,
    status_code=status.HTTP_201_CREATED,
)
def create_drill(
    drill: DrillCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.coach)),
):
    db_drill = Drill(
        **drill.dict(),
        # подготовка за следваща стъпка (ownership)
        # created_by=current_user.id,
        # club_id=current_user.club_id,
    )

    db.add(db_drill)
    db.commit()
    db.refresh(db_drill)

    return db_drill
