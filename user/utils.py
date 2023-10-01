import hashlib
from typing import Union, Any
from datetime import datetime, timedelta

from config import settings

from jose import jwt


def sha256_hash(string: str) -> str:
    """
    Hash string in sha256
    """
    return hashlib.sha256(string).hexdigest()


def compare_password(password: str, hashed_password: str) -> bool:
    """
    Compare password
    """
    return sha256_hash(password) == hashed_password


def create_access_token(object: Union[str, Any], expires_delta: int = None) -> str:
    """
    Create JWT token for user
    """
    if expires_delta:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(object)}
    jwt_encoded = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return jwt_encoded


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """
    Create JWT refresh token
    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_KEY, settings.ALGORITHM)
    return encoded_jwt
