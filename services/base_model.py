from datetime import datetime

from uuid import uuid4, UUID as UUID_TYPE

from .database import Base

from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class BaseUUIDModel(Base):
    """Abstact model with uuid and date_created"""

    __abstract__ = True

    uuid: Mapped[UUID_TYPE] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    date_created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
