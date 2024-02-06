from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text

import datetime

from src.database import Base, str_256


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str_256] = mapped_column(unique=False)
    name: Mapped[str_256] = mapped_column()
    hash_password: Mapped[str] = mapped_column()
    is_email_verified: Mapped[bool] = mapped_column(server_default=text("false"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('UTC', NOW())"))
    is_deleted: Mapped[bool] = mapped_column(server_default=text("false"), nullable=False)

    sessions: Mapped[list["Sessions"]] = relationship(
        back_populates="user"
    )

    categories: Mapped[list["Categories"]] = relationship(
        back_populates="user"
    )

