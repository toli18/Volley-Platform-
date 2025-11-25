from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.dependencies import get_db_session, require_role, get_current_user
from backend.app.models import Training, TrainingExercise, UserRole
from backend.app.schemas import TrainingCreateSchema, TrainingReadSchema

router = APIRouter(prefix="/trainings", tags=["trainings"])


@router.get("/", response_model=List[TrainingReadSchema])
def list_trainings(db: Session = Depends(get_db_session)):
    return db.query(Training).all()


@router.post(
    "/",
    response_model=TrainingReadSchema,
    dependencies=[
        Depends(
            require_role(UserRole.coach, UserRole.bfv_admin, UserRole.platform_admin)
        )
    ],
)
def create_training(
    payload: TrainingCreateSchema,
    db: Session = Depends(get_db_session),
    user=Depends(get_current_user),
):
    training = Training(
        club_id=payload.club_id,
        created_by=user.id,
        name=payload.name,
        description=payload.description,
        age_group=payload.age_group,
        total_duration_min=payload.total_duration_min,
    )
    db.add(training)
    db.commit()
    db.refresh(training)
    for item in payload.exercises:
        assoc = TrainingExercise(
            training_id=training.id,
            exercise_id=item.exercise_id,
            order_index=item.order_index,
            custom_duration_min=item.custom_duration_min,
            notes=item.notes,
        )
        db.add(assoc)
    db.commit()
    return training
