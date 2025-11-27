from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import User
from backend.app.security import verify_password, create_token, decode_token
from backend.app.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# --------------------------
# AUTHENTICATE USER
# --------------------------

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


# --------------------------
# CREATE ACCESS TOKEN
# --------------------------

def create_access_token(email: str) -> str:
    return create_token(email, expires_minutes=settings.access_token_expires_minutes)


# --------------------------
# CURRENT USER
# --------------------------

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    email = decode_token(token)

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
