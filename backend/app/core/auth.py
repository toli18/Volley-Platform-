from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.core.auth import authenticate_user, create_access_token
from backend.app.schemas import LoginRequest, Token, UserRead
from backend.app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint using email + password.
    Returns JWT access token.
    """

    # FIX: use credentials.email instead of credentials.username
    user = authenticate_user(db, credentials.email, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token({"sub": user.email})

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserRead)
def me(current_user: UserRead = Depends(get_current_user)):
    """
    Returns the currently authenticated user based on JWT token.
    """
    return current_user
