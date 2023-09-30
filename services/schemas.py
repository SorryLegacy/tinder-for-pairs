from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class UserNoPassword(BaseModel):
    uuid: UUID
    name: str
    username: str
    date_created: datetime


class User(UserNoPassword):
    password: str

    class Config:
        orm_mode = True
