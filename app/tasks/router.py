from fastapi import APIRouter, Depends, Query
from app.database import get_db
from app.core.deps import get_user_id
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import (
    CreateTaskRequest,
    CreateTaskResponse,
    GetTasksByProjectResponse,
    UpdateTask
)
from .service import TasksService


router = APIRouter(prefix='/tasks', tags=["Tasks"])

@router.post('/', response_model=CreateTaskResponse)
async def create_task(
    task: CreateTaskRequest,
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    return await TasksService.create_task(task, user_id, db)

@router.get('/project/{project_id}', response_model=list[GetTasksByProjectResponse])
async def get_tasks_by_project(
    project_id: int,
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db),
    per_page: int = Query(default=10, ge=1, le=100, description="Число задач на страницу"),
    page: int = Query(default=1, ge=1, description="Номер страницы")
):
    return await TasksService.get_tasks_by_project(project_id, user_id, db, per_page, page)

@router.patch('/{task_id}')
async def update_task(
    task_id: int,
    updated_info: UpdateTask,
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    return await TasksService.update_task(task_id, updated_info, user_id, db)

@router.delete('/{task_id}')
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):

    await TasksService.delete_task(task_id, user_id, db)

    return None