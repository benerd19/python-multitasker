from .schemas import (
    CreateSubtaskRequest,
    CreateSubtaskResponse,
    GetSubtasksResponse,
    UpdateSubtaskRequest,
    UpdateSubtaskResponse
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_user_id
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from .models import SubTasksTable
from sqlalchemy import select


router = APIRouter(prefix='/subtasks', tags=["Subtasks"])

@router.post('/tasks/{task_id}', response_model=CreateSubtaskResponse)
async def create_subtask(
    task_id: int,
    subtask_data: CreateSubtaskRequest,
    db: AsyncSession = Depends(get_db),
    user_id: id = Depends(get_user_id),
):
    subtask = SubTasksTable(
        **{**subtask_data.model_dump(), "owner_id": user_id, "task_id": task_id}
    )

    db.add(subtask)
    await db.commit()
    await db.refresh(subtask)

    return subtask


@router.get('/tasks/{task_id}', response_model=GetSubtasksResponse)
async def get_subtask_by_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    result = await db.execute(select(SubTasksTable).where(
        SubTasksTable.task_id == task_id,
        SubTasksTable.owner_id == user_id
    )) 

    tasks = result.scalars().all()

    return tasks

@router.patch('/{subtask_id}', response_model=UpdateSubtaskResponse)
async def update_subtask(
    subtask_id: int,
    subtask_data: UpdateSubtaskRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    result = await db.execute(select(SubTasksTable).where(
        SubTasksTable.id == subtask_id,
        SubTasksTable.user_id == user_id
    ))


    subtask = result.scalar_one_or_none()

    if (subtask is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    new_data = subtask_data.model_dump(exclude_unset=True)

    for field, value in new_data.items():
        setattr(subtask, field, value)

    await db.commit()
    await db.refresh(subtask)

    return subtask

@router.delete('/{subtask_id}')
async def delete_subtask(
    subtask_id: int, 
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    result = await db.execute(select(SubTasksTable).where(
        SubTasksTable.id == subtask_id,
        SubTasksTable.owner_id == user_id
    ))

    subtask = result.scalar_one_or_none()

    if (subtask is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await db.delete(subtask)
    await db.commit()

    return None