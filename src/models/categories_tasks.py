from src.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class CategoriesTasks(Base):
    __tablename__ = "categories_tasks"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True
    )
