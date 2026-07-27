from sqlalchemy import String, Date, ForeignKey

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.core.enums import Priorities

class TasksTable(Base): 
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    deadline: Mapped[date] = mapped_column(Date, nullable=True)
    label: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    priority: Mapped[Priorities]

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    owner: Mapped["UsersTable"] = relationship(back_populates="tasks")

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )
    project: Mapped["ProjectsTable"] = relationship(back_populates="tasks")

    subtasks: Mapped[list["SubTasksTable"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan"
    )