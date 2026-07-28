from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import Priorities
from app.database import Base


class SubTasksTable(Base):
    __tablename__ = 'subtasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    deadline: Mapped[date] = mapped_column(Date, nullable=True)
    label: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    priority: Mapped[Priorities]

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UsersTable"] = relationship(back_populates="subtasks")

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE")
    )
    task: Mapped["TasksTable"] = relationship(back_populates="subtasks")
