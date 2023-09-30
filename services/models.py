from .base_model import BaseUUIDModel

from sqlalchemy import Column
from sqlalchemy import String


class User(BaseUUIDModel):
    """
    User table
    """

    __tablename__ = "user_user"

    name: str = Column(String, nullable=False)
    password: str = Column(String, nullable=False)
    username: str = Column(String, nullable=False, unique=True)
