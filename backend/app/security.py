backend/app/core/auth.py
+38
-25

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import backend.app.security as security
from backend.app.config import settings
from backend.app.database import get_db
from backend.app.core.auth import authenticate_user, create_access_token
from backend.app.schemas import LoginRequest, Token, UserRead
from backend.app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])
from backend.app.models import User


@router.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint using email + password.
    Returns JWT access token.
    """
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    # FIX: use credentials.email instead of credentials.username
    user = authenticate_user(db, credentials.email, credentials.password)

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Validate a user's credentials using their email address."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not security.verify_password(password, user.password_hash):
        return None

    return user


def create_access_token(subject: str, expires_minutes: int = settings.access_token_expires_minutes) -> str:
    """Create a short-lived JWT access token for the given subject."""
    return security.create_token(subject, expires_minutes=expires_minutes)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """Retrieve the current user from a JWT bearer token."""
    subject = security.decode_token(token)
    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
            detail="Invalid authentication credentials",
        )

    access_token = create_access_token({"sub": user.email})

    return Token(access_token=access_token, token_type="bearer")

    user = db.query(User).filter(User.email == subject).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

@router.get("/me", response_model=UserRead)
def me(current_user: UserRead = Depends(get_current_user)):
    """
    Returns the currently authenticated user based on JWT token.
    """
    return current_user
    return user
backend/app/dependencies.py
+1
-15

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.core.auth import get_current_user
from backend.app.database import get_db
from backend.app.models import User, UserRole
from backend.app.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db_session() -> Generator:
    yield from get_db()


def get_current_user(db: Session = Depends(get_db_session), token: str = Depends(oauth2_scheme)) -> User:
    subject = decode_token(token)
    if subject is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.email == subject).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_role(*roles: UserRole):
    def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user

    return role_checker
backend/app/routers/auth.py
+14
-7

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.core.auth import authenticate_user, create_access_token, get_current_user
from backend.app.database import get_db
from backend.app.core.auth import authenticate_user, create_access_token
from backend.app.models import User
from backend.app.schemas import LoginRequest, Token
from backend.app.dependencies import get_current_user
from backend.app.schemas import Token, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user using username and password."""
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    access_token = create_access_token({"sub": user.email})
    access_token = create_access_token(user.email)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user."""
    return current_user
backend/app/security.py
+0
-29

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.app.config import settings
from backend.app.models import User
from sqlalchemy.orm import Session

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -----------------------------------------
# PASSWORD HELPERS
# -----------------------------------------

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# -----------------------------------------
# JWT TOKEN HELPERS
# -----------------------------------------

def create_token(subject: str, expires_minutes: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode = {"sub": subject, "exp": expire}

    return jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )


def decode_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        return payload.get("sub")

    except JWTError:
        return None


# -----------------------------------------
# NEW – REQUIRED BY CODEX AUTH ROUTER
# -----------------------------------------

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Validate username & password against DB.
    Returns the User object if valid, otherwise None.
    """
    user = db.query(User).filter(User.email == username).first()
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def create_access_token(data: dict) -> str:
    """
    Wrapper used by auth router. Always returns a JWT for 60 minutes.
    """
    subject = data.get("sub")
    return create_token(subject, expires_minutes=60)
