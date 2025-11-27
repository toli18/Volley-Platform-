from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.database import get_db
from backend.app.models import User
import backend.app.security as security

# Bearer схема за JWT токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ---------------------------
#  AUTHENTICATE USER
# ---------------------------

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Валидира email + парола срещу базата."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not security.verify_password(password, user.password_hash):
        return None

    return user


# ---------------------------
#  CREATE ACCESS TOKEN
# ---------------------------

def create_access_token(subject: str) -> str:
    """Създава кратко живеещ JWT access token за даден subject (email)."""
    return security.create_token(
        subject,
        expires_minutes=settings.access_token_expires_minutes,
    )


# ---------------------------
#  CURRENT USER
# ---------------------------

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """Връща текущия потребител на база Bearer JWT токена."""
    subject = security.decode_token(token)
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
