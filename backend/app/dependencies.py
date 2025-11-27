from typing import Generator
from fastapi import Depends, HTTPException, status

from backend.app.core.auth import get_current_user
from backend.app.database import get_db
from backend.app.models import User, UserRole


def get_db_session() -> Generator:
    yield from get_db()


def require_role(*roles: UserRole):
    def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user

    return role_checker
