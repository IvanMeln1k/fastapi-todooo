from src.database import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["Users"] = relationship(
        back_populates="categories"
    )

    tasks: Mapped["Tasks"] = relationship(
        back_populates="categories",
        secondary="categories_tasks"
    )

