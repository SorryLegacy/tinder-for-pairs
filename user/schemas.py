from typing import Optional
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, model_validator, field_validator, ConfigDict

from .utils import sha256_hash
from services.schemas import BaseShemasUUID


class UserAuth(BaseModel):
    username: str
    password: str

    @field_validator("password")
    def check_password_first(cls, password: str) -> str:
        if len(password) < 3:
            raise ValueError("Password must be greater than 3 symbols")
        return sha256_hash(password)


class UserRegister(UserAuth):
    name: str
    confirm_password: Optional[str] = None

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
    username: str
    date_created: datetime


class UserDB(UserNoPassword):
    password: str


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
