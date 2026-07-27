from sqlalchemy import String, ForeignKey

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ProjectsTable(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    label: Mapped[str] = mapped_column(String(255))

    tasks: Mapped[list["TasksTable"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("activity_categories.id", ondelete="CASCADE")
    )

    category: Mapped["ActivityCategoriesTable"] = relationship(
        back_populates="projects"
    )


    def __repr__(self):
        return f"<Project id={self.id} name='{self.name}'>"








