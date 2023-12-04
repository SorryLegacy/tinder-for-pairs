from typing import Optional, Sequence
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import (
    BaseModel,
    model_validator,
    field_validator,
    ConfigDict,
    Field,
    EmailStr,
)

from .utils import sha256_hash
from services.schemas import BaseShemasUUID


class UserAuth(BaseModel):
    login: str
    password: str

    @field_validator("password")
    def check_password_first(cls, password: str) -> str:
        if len(password) < 3:
            raise ValueError("Password must be greater than 3 symbols")
        return password


class UserRegister(BaseModel):
    name: str
    username: Optional[str]
    email: Optional[str]
    password: str
    confirm_password: Optional[str] = None

    @field_validator("password")
    def check_password_first(cls, password: str) -> str:
        if len(password) < 3:
            raise ValueError("Password must be greater than 3 symbols")
        return sha256_hash(password)

    @model_validator(mode="after")
    def check_password(cls, values: dict) -> dict:
        """
        Method to compare password and cashed they
        """

        password = values.password
        confirm_password = values.confirm_password
        if all((password, confirm_password)):
            if password == sha256_hash(confirm_password):
                del values.confirm_password
                return values
            else:
                raise ValueError("Provides diffrent passwords")
        raise ValueError("Password must be provided")


class UserNoPassword(BaseShemasUUID):
    model_config = ConfigDict(from_attributes=True)

    name: str
    username: Optional[str]
    date_created: datetime
    is_admin: bool
    email: Optional[str]


class UserCreateByAdmin(BaseModel):
    name: str
    username: Optional[str]
    is_admin: bool = Field(default=False)
    email: EmailStr


class ListUsers(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    users: Sequence[UserNoPassword]


class SignaturePayload(BaseModel):
    exp: int
    sub: str

    @field_validator("exp")
    def validate_expartion_data(cls, exp: int) -> int:
        if datetime.fromtimestamp(exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return exp


class TokenResposnse(BaseModel):
    access_token: str
    refresh_token: str


class ResetPassword(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def compare_password(cls, values: dict) -> dict:
        if values.password == values.confirm_password:
            values.password = sha256_hash(values.password)
            return values
        raise ValueError("Provides diffrent passwords")
