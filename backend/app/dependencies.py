from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import User, UserRole
from backend.app.core.auth import get_current_user


def get_db_session() -> Generator[Session, None, None]:
    """Общ зависимост за достъп до DB Session."""
    yield from get_db()


def require_role(*roles: UserRole):
    """
    Dependency, което гарантира, че текущия потребител има една от зададените роли.
    Пример:
        @router.get("/admin-only")
        def admin_endpoint(user: User = Depends(require_role(UserRole.admin))):
            ...
    """

    def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return role_checker
