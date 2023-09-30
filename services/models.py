from datetime import datetime

from .base_model import BaseUUIDModel

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func


class User(BaseUUIDModel):
    """
    User table
    """

    __tablename__ = "user_user"

    name: str = Column(String, nullable=False)
    password: str = Column(String, nullable=False)
    username: str = Column(String, nullable=False, unique=True)
    date_created: datetime = Column(DateTime, nullable=False, default=func.now())
