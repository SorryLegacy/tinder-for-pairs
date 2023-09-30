from uuid import UUID
from pydantic import BaseModel


class UserNoPassword(BaseModel):
    uuid: UUID
    name: str
    username: str


class User(UserNoPassword):
    password: str

    class Config:
        orm_mode = True
