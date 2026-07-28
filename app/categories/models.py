from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ActivityCategoriesTable(Base):
    __tablename__ = 'activity_categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    color: Mapped[str] = mapped_column(String(7))
    description: Mapped[str] = mapped_column(String(255))

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    user: Mapped["UsersTable"] = relationship(back_populates="categories")

    projects: Mapped[list["ProjectsTable"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan"
    )

    

    def __repr__(self):
        return f"<ActivityCategory id={self.id} name='{self.name}'>"