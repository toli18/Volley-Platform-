from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.app.dependencies import get_db_session, get_current_user
from backend.app.models import User, UserRole
from backend.app.schemas import LoginRequestSchema, TokenSchema, UserReadSchema
from backend.app.security import create_token, verify_password
from backend.app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenSchema)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session),
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = create_token(user.email, settings.access_token_expires_minutes)
    refresh_token = create_token(user.email, settings.refresh_token_expires_minutes)
    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UserReadSchema)
def me(current_user: User = Depends(get_current_user)):
    return current_user
