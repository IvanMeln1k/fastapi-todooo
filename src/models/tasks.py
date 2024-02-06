from src.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    done: Mapped[bool] = mapped_column()

    categories: Mapped[list["Categories"]] = relationship(
        back_populates="tasks",
        secondary="categories_tasks"
    )
