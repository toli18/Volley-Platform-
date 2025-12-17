from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.dependencies.roles import require_role
from backend.app.models import Drill, DrillStatus, UserRole
from backend.app.schemas.drill import (
    DrillCreate,
    DrillRead,
    DrillUpdateStatus,
)

router = APIRouter()


# =========================
# GET all drills (public)
# =========================
@router.get("/", response_model=list[DrillRead])
def get_drills(db: Session = Depends(get_db)):
    return (
        db.query(Drill)
        .filter(Drill.status == DrillStatus.approved)
        .all()
    )


# =========================
# GET drill by id (public)
# =========================
@router.get("/{drill_id}", response_model=DrillRead)
def get_drill(drill_id: int, db: Session = Depends(get_db)):
    drill = (
        db.query(Drill)
        .filter(
            Drill.id == drill_id,
            Drill.status == DrillStatus.approved,
        )
        .first()
    )

    if not drill:
        raise HTTPException(status_code=404, detail="Drill not found")

    return drill


# =========================
# CREATE drill (coach)
# =========================
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
        status=DrillStatus.draft,
    )

    db.add(db_drill)
    db.commit()
    db.refresh(db_drill)

    return db_drill


# =========================
# UPDATE drill status (bfv_admin)
# =========================
@router.patch("/{drill_id}/status", response_model=DrillRead)
def update_drill_status(
    drill_id: int,
    payload: DrillUpdateStatus,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role(UserRole.admin, UserRole.bfv_admin)
    ),
):
    drill = db.query(Drill).filter(Drill.id == drill_id).first()

    if not drill:
        raise HTTPException(status_code=404, detail="Drill not found")

    drill.status = payload.status
    db.commit()
    db.refresh(drill)

    return drill

