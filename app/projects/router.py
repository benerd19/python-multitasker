from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from .schemas import (
    ProjectResponse, 
    ProjectCreateRequest, 
    ProjectCreateResponse, 
    ProjectUpdateRequest, 
    ProjectUpdateResponse, 
    )
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import ProjectsTable
from app.core.deps import get_user_id
from app.categories.models import ActivityCategoriesTable

router = APIRouter(prefix='/projects', tags=['Projects'])

#PROJECTS
@router.get('/', response_model=list[ProjectResponse])
async def get_projects(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
    ):
    result = await db.execute(select(ProjectsTable).join(ActivityCategoriesTable).where(ActivityCategoriesTable.user_id == user_id))
    projects = result.scalars().unique().all() 

    return projects

@router.post('/', response_model=ProjectCreateResponse)
async def create_project(
    db: AsyncSession = Depends(get_db), 
    user_id: int = Depends(get_user_id),
    project: ProjectCreateRequest = None
    ):

    project_data = project.model_dump()
    result = await db.execute(select(ActivityCategoriesTable).where(ActivityCategoriesTable.user_id == user_id, ActivityCategoriesTable.id == project_data["category_id"]))

    categories = result.scalar_one_or_none()


    if (categories is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    new_project = ProjectsTable(**project_data)

    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)

    return new_project

@router.patch('/{project_id}', response_model=ProjectUpdateResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    result = await db.execute(select(ProjectsTable).join(ActivityCategoriesTable).where(ProjectsTable.id == project_id, ActivityCategoriesTable.user_id == user_id))

    project = result.scalar_one_or_none()

    if (project is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    updated_data = project_data.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(project, field, value)

    await db.commit()
    await db.refresh(project)

    return project

@router.delete('/{project_id}')
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    result = await db.execute(select(ProjectsTable).join(ActivityCategoriesTable).where(ProjectsTable.id == project_id, ActivityCategoriesTable.user_id == user_id))

    project = result.scalar_one_or_none()

    if (project is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    await db.delete(project)
    await db.commit()

    return None


    

    
    

