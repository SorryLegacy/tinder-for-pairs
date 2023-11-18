from uuid import UUID
from pydantic import BaseModel


class BaseShemasUUID(BaseModel):
    uuid: UUID


class TokenResposnse(BaseModel):
    access_token: str
    refresh_token: str
