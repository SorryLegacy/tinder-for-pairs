from uuid import UUID
from pydantic import BaseModel


class BaseShemasUUID(BaseModel):
    uuid: UUID
