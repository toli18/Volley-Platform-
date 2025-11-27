from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.database import get_db
from backend.app.models import User
from backend.app.security import decode_token, verify_password, create_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Validate a user's credentials using their email address."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def create_access_token(subject: str, expires_minutes: int = settings.access_token_expires_minutes) -> str:
    """Create a short-lived JWT access token for the given subject."""
    return create_token(subject, expires_minutes=expires_minutes)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """Retrieve the current user from a JWT bearer token."""
    subject = decode_token(token)
    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = db.query(User).filter(User.email == subject).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
