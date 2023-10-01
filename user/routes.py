from app import app
from services.database import create_session

from .models import User
from .schemas import UserNoPassword, UserAuth

from sqlalchemy import exists

from fastapi import status, HTTPException


@app.post("/signup", summary="Create new user in system", response_model=UserNoPassword)
async def create_user(data: UserAuth) -> UserNoPassword:
    with create_session() as session:
        query = exists().where(User.username == data.username)  # TODO check row
        if session.execute(query):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username exists",
            )
    pass
