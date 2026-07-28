from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import PyJWTError
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(hashed_password: str, plain_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_tokens(data: dict) -> tuple[str, str]:
    access_data = data.copy()
    refresh_data = data.copy()

    expire_access = datetime.now(timezone.utc) + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_refresh = datetime.now(timezone.utc) + timedelta(minutes = settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    access_data.update({"exp": expire_access})
    refresh_data.update({"exp": expire_refresh})

    access_token = jwt.encode(payload=access_data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    refresh_token = jwt.encode(payload=refresh_data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return access_token, refresh_token

def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except PyJWTError:
        return None