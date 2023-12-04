from uuid import uuid4

from .database import Base

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID


class BaseUUIDModel(Base):
    """abstact model"""

    __abstract__ = True

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
