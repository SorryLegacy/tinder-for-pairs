from urllib.parse import urljoin

from config import settings
from services.database import db_depends

from .models import User
from .utils import (
    create_access_token,
    create_refresh_token,
    compare_password,
    generate_random_string,
    sha256_hash,
    send_email,
)
from .schemas import (
    UserRegister,
    TokenResposnse,
    UserNoPassword,
    UserAuth,
    SignaturePayload,
    ListUsers,
    UserCreateByAdmin,
    ResetPassword,
)
from .deps import get_current_user, admin_only, verify_token

from sqlalchemy import exists, select, or_

from jose import jwt, JWTError
from pydantic import ValidationError
from fastapi import (
    status,
    HTTPException,
    APIRouter,
    Depends,
    Request,
    Response,
    BackgroundTasks,
)


router = APIRouter()


@router.post(
    "/signup", summary="Create new user in system", response_model=TokenResposnse
)
async def create_user(data: UserRegister, db: db_depends) -> TokenResposnse:
    """
    View to create user and add tokens
    """
    try:
        query = select(
            exists().where(
                or_(User.username == data.username, User.email == data.email)
            )
        )
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
async def login(db: db_depends, response: Response, data: UserAuth) -> TokenResposnse:
    """
    Login in system
    """
    try:
        query = select(User).where(
            or_(User.username == data.login, User.email == data.login)
        )
        user = db.execute(query).scalar()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username"
            )
        if not compare_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password"
            )
        response_dict = {
            "access_token": create_access_token(data.login),
            "refresh_token": create_refresh_token(data.login),
        }
        response.set_cookie(
            key="refresh_token", value=response_dict.get("refresh_token"), httponly=True
        )
        return response_dict
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/refresh_token", summary="Refresh JWT token", response_model=TokenResposnse
)
async def refresh_token(
    request: Request,
    has_token: SignaturePayload = Depends(verify_token),  # noqa f722
) -> TokenResposnse:
    """
    Refresh jwt token
    """
    if refresh_token := request.cookies.get("refresh_token"):
        try:
            payload = jwt.decode(
                refresh_token, settings.JWT_REFRESH_KEY, algorithms=settings.ALGORITHM
            )
            signature = SignaturePayload(**payload)
        except (JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Not correct token"
            )
        response = {
            "access_token": create_access_token(signature.sub),
            "refresh_token": refresh_token,
        }
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated"
        )


@router.get("/me", summary="Info about current User", response_model=UserNoPassword)
async def me(user: UserNoPassword = Depends(get_current_user)):
    return user


@router.get(
    "/api/v1/users",
    summary="Admin only; return list of users",
    response_model=ListUsers,
)
async def list_users(
    db: db_depends, user: UserNoPassword = Depends(admin_only)
) -> ListUsers:
    users = [
        value for (value,) in db.execute(select(User)).fetchall()
    ]  # TODO probably fix
    return ListUsers.model_validate({"users": users})


@router.post(
    "/api/v1/users", summary="Admin only; create user", response_model=UserNoPassword
)
async def create_user_admin(
    user_data: UserCreateByAdmin,
    db: db_depends,
    backgroud_task: BackgroundTasks,
    request: Request,
    user: UserNoPassword = Depends(admin_only),
) -> UserNoPassword:
    query = select(
        exists().where(
            or_(User.username == user_data.username, User.email == user_data.email)
        )
    )
    if db.execute(query).scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with sush email/username exists",
        )
    password = sha256_hash(generate_random_string())
    new_user = User(
        email=user_data.email,
        password=password,
        is_admin=user_data.is_admin,
        name=user_data.name,
        username=user_data.username,
    )
    db.add(new_user)
    access_token = create_access_token(user_data.email, 3600)
    email_message = urljoin(str(request.base_url), f"/restore-password/{access_token}")
    print(email_message)
    backgroud_task.add_task(send_email, user_data.email, email_message)
    db.commit()
    return UserNoPassword.model_validate(new_user)


@router.post("/restore-password/{jwt_string}", response_model=bool)
async def restore_password(
    db: db_depends, jwt_string: str, user_password: ResetPassword
):
    try:
        payload = jwt.decode(
            jwt_string, settings.JWT_SECRET_KEY, algorithms=settings.ALGORITHM
        )
        signature = SignaturePayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated"
        )
    else:
        query_user = select(User).where(User.email == signature.sub)
        if user := db.execute(query_user).scalar():
            user.password = user_password.password
            db.commit()
            return Response(status_code=status.HTTP_200_OK)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated"
        )
