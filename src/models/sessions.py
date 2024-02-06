from src.database import Base, str_32

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

import datetime


class Sessions(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str_32] = mapped_column()
    expires_in: Mapped[datetime.datetime] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["Users"] = relationship(
        back_populates="sessions"
    )
