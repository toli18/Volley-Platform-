from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import Drill
from backend.app.schemas.drill import DrillCreate, DrillRead

router = APIRouter(prefix="/drills", tags=["Drills"])


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
        query = query.filter(Drill.age_min <= age, Drill.age_max >= age)
    if skill:
        query = query.filter(Drill.skill_domains.ilike(f"%{skill}%"))
    if phase:
        query = query.filter(Drill.game_phases.ilike(f"%{phase}%"))

    return query.all()


@router.get("/{drill_id}", response_model=DrillRead)
def get_drill(drill_id: int, db: Session = Depends(get_db)):
    return db.query(Drill).get(drill_id)


@router.post("/", response_model=DrillRead)
def create_drill(drill: DrillCreate, db: Session = Depends(get_db)):
    db_drill = Drill(**drill.dict())
    db.add(db_drill)
    db.commit()
    db.refresh(db_drill)
    return db_drill
