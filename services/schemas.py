from uuid import UUID
from pydantic import BaseModel, Field


class BaseShemasUUID(BaseModel):
    uuid: UUID = Field(alias="id")
