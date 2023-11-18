from datetime import datetime

from services.base_model import BaseUUIDModel

from sqlalchemy import String
from sqlalchemy import DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class User(BaseUUIDModel):
    """
    User table
    """

    __tablename__ = "user_user"

    name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    date_created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
