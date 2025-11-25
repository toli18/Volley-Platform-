from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from backend.app.dependencies import get_current_user, get_db_session
from backend.app.models import Exercise, Training, TrainingExercise, User, UserRole
from backend.app.schemas import (
    TrainingCreateSchema,
    TrainingExerciseCreateSchema,
    TrainingReadSchema,
    TrainingUpdateSchema,
)

router = APIRouter(prefix="/trainings", tags=["trainings"])


def _authorize_training_access(user: User, club_id: int) -> None:
    if user.role in (UserRole.platform_admin, UserRole.bfv_admin):
        return
    if user.role == UserRole.coach and user.club_id == club_id:
        return
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


def _validate_training_exercises(
    db: Session, exercises: List[TrainingExerciseCreateSchema]
) -> None:
    order_indexes = [item.order_index for item in exercises]
    if len(order_indexes) != len(set(order_indexes)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duplicate order_index values are not allowed",
        )

    exercise_ids = [item.exercise_id for item in exercises]
    if not exercise_ids:
        return
    existing_ids = {
        row[0]
        for row in db.query(Exercise.id).filter(Exercise.id.in_(exercise_ids)).all()
    }
    missing_ids = set(exercise_ids) - existing_ids
    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercises not found: {sorted(missing_ids)}",
        )


def _get_training_with_exercises(db: Session, training_id: int) -> Optional[Training]:
    return (
        db.query(Training)
        .options(joinedload(Training.exercises).joinedload(TrainingExercise.exercise))
        .filter(Training.id == training_id)
        .first()
    )


@router.get("/", response_model=List[TrainingReadSchema])
def list_trainings(
    club_id: Optional[int] = None, db: Session = Depends(get_db_session)
):
    query = db.query(Training).options(
        joinedload(Training.exercises).joinedload(TrainingExercise.exercise)
    )
    if club_id is not None:
        query = query.filter(Training.club_id == club_id)
    return query.all()


@router.get("/{training_id}", response_model=TrainingReadSchema)
def get_training(training_id: int, db: Session = Depends(get_db_session)):
    training = _get_training_with_exercises(db, training_id)
    if not training:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return training


@router.post("/", response_model=TrainingReadSchema)
def create_training(
    payload: TrainingCreateSchema,
    db: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    _authorize_training_access(user, payload.club_id)
    _validate_training_exercises(db, payload.exercises)

    training = Training(
        club_id=payload.club_id,
        created_by=user.id,
        name=payload.name,
        description=payload.description,
        age_group=payload.age_group,
        total_duration_min=payload.total_duration_min,
    )
    db.add(training)
    db.flush()

    for item in payload.exercises:
        db.add(
            TrainingExercise(
                training_id=training.id,
                exercise_id=item.exercise_id,
                order_index=item.order_index,
                custom_duration_min=item.custom_duration_min,
                notes=item.notes,
            )
        )

    db.commit()
    return _get_training_with_exercises(db, training.id)


@router.put("/{training_id}", response_model=TrainingReadSchema)
def update_training(
    training_id: int,
    payload: TrainingUpdateSchema,
    db: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    training = _get_training_with_exercises(db, training_id)
    if not training:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    _authorize_training_access(user, training.club_id)

    if payload.exercises is not None:
        _validate_training_exercises(db, payload.exercises)

    if payload.name is not None:
        training.name = payload.name
    if payload.description is not None:
        training.description = payload.description
    if payload.age_group is not None:
        training.age_group = payload.age_group
    if payload.total_duration_min is not None:
        training.total_duration_min = payload.total_duration_min

    if payload.exercises is not None:
        db.query(TrainingExercise).filter(
            TrainingExercise.training_id == training.id
        ).delete()
        for item in payload.exercises:
            db.add(
                TrainingExercise(
                    training_id=training.id,
                    exercise_id=item.exercise_id,
                    order_index=item.order_index,
                    custom_duration_min=item.custom_duration_min,
                    notes=item.notes,
                )
            )

    db.commit()
    return _get_training_with_exercises(db, training.id)


@router.delete("/{training_id}")
def delete_training(
    training_id: int,
    db: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    training = db.query(Training).filter(Training.id == training_id).first()
    if not training:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    _authorize_training_access(user, training.club_id)

    db.query(TrainingExercise).filter(
        TrainingExercise.training_id == training.id
    ).delete()
    db.delete(training)
    db.commit()
    return {"status": "deleted"}
