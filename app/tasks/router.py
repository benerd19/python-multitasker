from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.core.deps import get_user_id
from .models import TasksTable
from app.projects.models import ProjectsTable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import (
    CreateTaskRequest,
    CreateTaskResponse,
    GetTasksByProjectResponse,
    UpdateTask
)


router = APIRouter(prefix='/tasks', tags=["Tasks"])

@router.post('/{project_id}/tasks', response_model=CreateTaskResponse)
async def create_task(
    project_id: int,
    task: CreateTaskRequest,
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ProjectsTable).where(ProjectsTable.id == project_id))

    project = result.scalar_one_or_none()

    if (project is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    new_task = TasksTable(
        deadline=task.deadline,
        label=task.label,
        description=task.description,
        priority=task.priority,
        owner_id=user_id,
        project_id=project.id
    )

    db.add(new_task)

    await db.commit()
    await db.refresh(new_task)

    return new_task

@router.get('/{project_id}/tasks', response_model=list[GetTasksByProjectResponse])
async def get_tasks_by_project(
    project_id: int,
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(TasksTable).where(
        TasksTable.project_id == project_id, 
        TasksTable.owner_id == user_id
        ))

    tasks = result.scalars().all()

    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    

    return tasks

@router.patch('/{project_id}/tasks/{task_id}')
async def update_task(
    project_id: int,
    task_id: int,
    updated_info: UpdateTask,
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(TasksTable).where(TasksTable.id == task_id))

    task = result.scalar_one_or_none()

    if (task is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    updated_data = {**updated_info.model_dump(exclude_unset=True), "project_id": project_id, "owner_id": user_id}

    for field, value in updated_data.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)

    return task    

@router.delete('/{project_id}/tasks/{task_id}')
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    result = await db.execute(select(TasksTable).where(TasksTable.id == task_id, TasksTable.owner_id == user_id))

    task = result.scalar_one_or_none()

    if (task is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    await db.delete(task)
    await db.commit()

    return None