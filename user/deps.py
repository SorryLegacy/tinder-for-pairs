from config import settings
from services.database import db_depends
from .models import User
from .schemas import UserNoPassword, SignaturePayload

from jose import jwt
from pydantic import ValidationError
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy import select, or_


async def verify_token(
    access_token: str = Header(..., convert_underscores=False)
) -> SignaturePayload:
    try:
        signature = jwt.decode(
            access_token, settings.JWT_SECRET_KEY, algorithms=settings.ALGORITHM
        )
        token_data = SignaturePayload(**signature)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data


async def get_current_user(
    db: db_depends, token_data: SignaturePayload = Depends(verify_token)
) -> UserNoPassword:
    """
    Validate JWT token and return current user
    """
    query = select(User).where(
        or_(User.username == token_data.sub, User.email == token_data.sub)
    )
    user = db.execute(query).scalar()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not find user"
        )
    return UserNoPassword.model_validate(user)


async def admin_only(user: UserNoPassword = Depends(get_current_user)):
    if user.is_admin:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Dont have permission"
    )
