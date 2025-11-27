from typing import Optional
from sqlalchemy.orm import Session

from backend.app.models import User
from backend.app.security import verify_password, create_access_token as _create_access_token, decode_token
from backend.app.database import get_db


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Validate username+password and return user or None."""
    user = db.query(User).filter(User.email == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict) -> str:
    """Wrapper for security.create_access_token"""
    return _create_access_token(data)
