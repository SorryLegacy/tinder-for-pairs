from config import settings
from services.database import db_depends
from .models import User
from .schemas import UserNoPassword, SignaturePayload

from jose import jwt
from pydantic import ValidationError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


async def get_current_user(
    db: db_depends, token: str = Depends(reuseable_oauth)
) -> UserNoPassword:
    """
    Validate JWT token and return current user
    """
    try:
        signature = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=settings.ALGORITHM
        )
        token_data = SignaturePayload(**signature)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    query = select(User).where(User.username == token_data.sub)
    user = db.execute(query).scalar()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not find user"
        )
    return UserNoPassword.model_validate(user)
