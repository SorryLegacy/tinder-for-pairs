from datetime import datetime

from services.schemas import BaseShemasUUID

from pydantic import BaseModel


class UserAuth(BaseModel):
    name: str
    username: str
    password: str


class UserNoPassword(BaseShemasUUID):
    name: str
    username: str
    date_created: datetime


class UserDB(UserNoPassword):
    password: str

    class Config:
        orm_mode = True
