from datetime import datetime, timedelta
from jose import jwt

from backend.app.settings import settings

ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 30


def create_access_token(subject: str):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    return jwt.encode(
        {"exp": expire, "sub": str(subject)}, settings.SECRET_KEY, algorithm="HS256"
    )


def create_refresh_token(subject: str):
    expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    expire = datetime.utcnow() + expires_delta
    return jwt.encode(
        {"exp": expire, "sub": str(subject)}, settings.SECRET_KEY, algorithm="HS256"
    )


def decode_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
