from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class BaseShemasUUID(BaseModel):
    uuid: UUID
    date_created: datetime
