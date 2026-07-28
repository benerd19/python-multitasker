from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_user_id
from app.database import get_db

from .schemas import (
    ProjectCreateRequest,
    ProjectCreateResponse,
    ProjectResponse,
    ProjectUpdateRequest,
    ProjectUpdateResponse,
)
from .service import ProjectService

router = APIRouter(prefix='/projects', tags=['Projects'])

#PROJECTS
@router.get('/', response_model=list[ProjectResponse])
async def get_projects(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
    ):
    return await ProjectService.get_projects(db, user_id)

    

@router.post('/', response_model=ProjectCreateResponse)
async def create_project(
    db: AsyncSession = Depends(get_db), 
    user_id: int = Depends(get_user_id),
    project: ProjectCreateRequest = None
    ):
    return await ProjectService.create_project(db, user_id, project)

@router.patch('/{project_id}', response_model=ProjectUpdateResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    return await ProjectService.update_project(db, project_id, user_id, project_data)

@router.delete('/{project_id}')
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    await ProjectService.delete_project(project_id, db, user_id)


    

    
    

