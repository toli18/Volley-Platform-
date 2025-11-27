from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.auth import get_current_user
from backend.app.database import get_db
from backend.app.models import UserRole, User


def require_role(*roles: UserRole):
    def checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user

    return checker
