from uuid import UUID

from services.base_model import BaseUUIDModel

from user.models import User

from sqlalchemy import ForeignKey, Uuid, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB


class Match(BaseUUIDModel):
    """
    Match model for user's
    """

    __tablename__ = "match"

    user_1_uuid: Mapped[UUID] = mapped_column(Uuid, ForeignKey("user_user.uuid"))
    user_1: Mapped["User"] = relationship("User", back_populates="main_user")
    user_2_uuid: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("user_user.uuid"), nullable=True
    )
    user_2: Mapped["User"] = relationship("User", back_populates="invited_user")
    is_match: Mapped[bool] = mapped_column(Boolean, default=False)
    data: Mapped[JSONB] = mapped_column(JSONB, nullable=True)
