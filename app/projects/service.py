from sqlalchemy.ext.asyncio import AsyncSession
from .models import ProjectsTable
from sqlalchemy import select
from app.categories.models import ActivityCategoriesTable
from .schemas import (
    ProjectCreateRequest
)
from fastapi import HTTPException, status

class ProjectService: 

    @staticmethod
    async def get_projects(
        db: AsyncSession,
        user_id: int
    ):
        result = await db.execute(
            select(ProjectsTable)
            .join(ActivityCategoriesTable)
            .where(ActivityCategoriesTable.user_id == user_id)

        )

        categories = result.scalars().unique().all()
        return list(categories)

    @staticmethod
    async def create_project(
        db: AsyncSession,
        user_id: int,
        project_data: ProjectCreateRequest
    ):
        category_result = await db.execute(
            select(ActivityCategoriesTable)
            .where(ActivityCategoriesTable.id == project_data.category_id,
                   ActivityCategoriesTable.user_id == user_id
            )
        )

        category = category_result.scalar_one_or_none()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )

        new_project = ProjectsTable(**project_data.model_dump())

        db.add(new_project)
        await db.commit()
        await db.refresh(new_project)

        return new_project

        

    @staticmethod
    async def update_project(
        db: AsyncSession,
        project_id: int,
        user_id: int,
        project_data: ProjectCreateRequest
    ):

        result = await db.execute(
            select(ProjectsTable)
            .join(ActivityCategoriesTable)
            .where(
                ProjectsTable.id == project_id,
                ActivityCategoriesTable.user_id == user_id
            )
        )

        project = result.scalar_one_or_none()

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

        update_data = project_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(project, field, value)

        await db.commit()
        await db.refresh(project)

        return project

    @staticmethod
    async def delete_project(
         project_id: int,
        db: AsyncSession,
        user_id: int
    ):
        result = await db.execute(select(ProjectsTable).join(ActivityCategoriesTable).where(ProjectsTable.id == project_id, ActivityCategoriesTable.user_id == user_id))
        
        project = result.scalar_one_or_none()
        
        if (project is None):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
        await db.delete(project)
        await db.commit()

        return None