from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UsersTable(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    avatar: Mapped[str] = mapped_column(String(255))

    tasks: Mapped[list["TasksTable"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    subtasks: Mapped[list["SubTasksTable"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    categories: Mapped[list["ActivityCategoriesTable"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User id={self.id} name='{self.name}'>"
    
    
