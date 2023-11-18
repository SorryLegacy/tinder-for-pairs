from typing import Optional
from datetime import datetime

from pydantic import BaseModel, model_validator, field_validator

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
    name: str
    username: str
    date_created: datetime


class UserDB(UserNoPassword):
    password: str

    class Config:
        orm_mode = True
