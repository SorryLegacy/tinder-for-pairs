from datetime import datetime

from services.base_model import BaseUUIDModel

from sqlalchemy import String, DateTime, Boolean, CheckConstraint, or_
from sqlalchemy_utils import EmailType
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column


class User(BaseUUIDModel):
    """
    User table
    """

    __tablename__ = "user_user"

    name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(
        String, nullable=True, unique=True, index=True
    )
    date_created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    email: Mapped[str] = mapped_column(
        EmailType, index=True, unique=True, nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            or_(username is not None, email is not None),
            name="username_or_email_required",
        ),
    )
