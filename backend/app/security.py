from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from backend.app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔥 FIX 1 — return the missing function
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 🔥 FIX 2 — this one is also expected by some routers
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# TOKEN HELPERS (already should exist, but leave them untouched)
def create_access_token(subject: str, expires_minutes: int = 60):
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload.get("sub")
    except JWTError:
        return None
