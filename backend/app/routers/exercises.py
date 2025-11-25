from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.dependencies import get_db_session, require_role, get_current_user
from backend.app.models import Exercise, ExerciseSuggestion, User, UserRole
from backend.app.schemas import (
    ExerciseCreateSchema,
    ExerciseReadSchema,
    ExerciseSuggestionCreateSchema,
    ExerciseSuggestionReadSchema,
)

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/", response_model=List[ExerciseReadSchema])
def list_exercises(
    db: Session = Depends(get_db_session),
    category: str | None = None,
    age: str | None = None,
    intensity: str | None = None,
):
    query = db.query(Exercise)
    if category:
        query = query.filter(Exercise.main_category == category)
    if intensity:
        query = query.filter(Exercise.intensity == intensity)
    # age filter simplified: checks containment in JSON array if provided
    if age:
        query = query.filter(Exercise.age_groups.contains([age]))
    return query.all()


@router.post(
    "/",
    response_model=ExerciseReadSchema,
    dependencies=[Depends(require_role(UserRole.platform_admin, UserRole.bfv_admin))],
)
def create_exercise(
    payload: ExerciseCreateSchema,
    db: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    exercise = Exercise(**payload.dict(), created_by=user.id, approved_by_admin=user.id)
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


@router.post(
    "/{exercise_id}/approve",
    response_model=ExerciseReadSchema,
    dependencies=[Depends(require_role(UserRole.bfv_admin, UserRole.platform_admin))],
)
def approve_exercise(
    exercise_id: int,
    db: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    exercise.approved_by_admin = user.id
    db.commit()
    db.refresh(exercise)
    return exercise


@router.post(
    "/suggestions",
    response_model=ExerciseSuggestionReadSchema,
    dependencies=[
        Depends(
            require_role(UserRole.coach, UserRole.bfv_admin, UserRole.platform_admin)
        )
    ],
)
def propose_exercise(
    payload: ExerciseSuggestionCreateSchema,
    db: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    suggestion = ExerciseSuggestion(
        name=payload.name,
        main_category=payload.main_category,
        description=payload.description,
        submitted_by=user.id,
        status="pending",
    )
    db.add(suggestion)
    db.commit()
    db.refresh(suggestion)
    return suggestion


@router.post(
    "/suggestions/{suggestion_id}/approve",
    response_model=ExerciseReadSchema,
    dependencies=[Depends(require_role(UserRole.bfv_admin, UserRole.platform_admin))],
)
def approve_suggestion(
    suggestion_id: int,
    db: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    suggestion = (
        db.query(ExerciseSuggestion)
        .filter(ExerciseSuggestion.id == suggestion_id)
        .first()
    )
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    exercise = Exercise(
        name=suggestion.name,
        main_category=suggestion.main_category or "general",
        description=suggestion.description,
        created_by=suggestion.submitted_by,
        approved_by_admin=user.id,
    )
    db.add(exercise)
    suggestion.status = "approved"
    suggestion.reviewed_by = user.id
    db.commit()
    db.refresh(exercise)
    return exercise
