from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.security import get_current_user as auth_get_current_user
from backend.app.database import get_db
from backend.app.models import User, UserRole


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# 🔥 Wrapper for backward compatibility
def get_db_session() -> Generator:
    """Compatibility wrapper used by old routers."""
    yield from get_db()


def get_current_user(
    db: Session = Depends(get_db_session),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Uses the unified authentication logic from security.py."""
    return auth_get_current_user(db=db, token=token)


def require_role(*roles: UserRole):
    """Dependency that ensures the authenticated user has specific roles."""

    def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user

    return role_checker
