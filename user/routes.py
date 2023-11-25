from services.database import db_depends

from .models import User
from .utils import create_access_token, create_refresh_token, compare_password
from .schemas import UserRegister, TokenResposnse, UserNoPassword
from .deps import get_current_user

from sqlalchemy import exists, select

from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post(
    "/signup", summary="Create new user in system", response_model=TokenResposnse
)
async def create_user(data: UserRegister, db: db_depends) -> TokenResposnse:
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
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", summary="Login in system", response_model=TokenResposnse)
async def login(
    db: db_depends, data: OAuth2PasswordRequestForm = Depends()
) -> TokenResposnse:
    """
    Login in system
    """
    try:
        query = select(User).where(User.username == data.username)
        user = db.execute(query).scalar()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username"
            )
        if not compare_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password"
            )

        response = {
            "access_token": create_access_token(data.username),
            "refresh_token": create_refresh_token(data.username),
        }
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", summary="Info about current User", response_model=UserNoPassword)
async def me(user: UserNoPassword = Depends(get_current_user)):
    return user
