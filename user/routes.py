from services.schemas import TokenResposnse
from services.database import get_db

from .models import User
from .utils import create_access_token, create_refresh_token
from .schemas import UserAuth, UserRegister


from sqlalchemy import exists, select

from typing import Annotated, Any
from fastapi import status, HTTPException, APIRouter, Depends


router = APIRouter()


@router.post(
    "/signup", summary="Create new user in system", response_model=TokenResposnse
)
async def create_user(
    data: UserRegister, db: Annotated[Any, Depends(get_db)]
) -> TokenResposnse:
    """
    View to create user and add tokens
    """
    try:
        query = select(exists().where(User.username == data.username))
        if db.execute(query).scalar():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username exists",
            )
        new_user = User(**data.model_dump())
        db.add(new_user)
        db.commit()
        response = {
            "access_token": create_access_token(new_user.username),
            "refresh_token": create_refresh_token(new_user.username),
        }
        return TokenResposnse(**response)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", summary="Login in system", response_model=TokenResposnse)
async def login(data: UserAuth) -> TokenResposnse:
    """
    Login in system
    """
    try:
        ...
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
