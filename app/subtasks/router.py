from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_user_id
from app.database import get_db

from .schemas import (
    CreateSubtaskRequest,
    CreateSubtaskResponse,
    GetSubtasksResponse,
    UpdateSubtaskRequest,
    UpdateSubtaskResponse,
)
from .service import SubtasksService

router = APIRouter(prefix='/subtasks', tags=["Subtasks"])

@router.post('/tasks/{task_id}', response_model=CreateSubtaskResponse)
async def create_subtask(
    task_id: int,
    subtask_data: CreateSubtaskRequest,
    db: AsyncSession = Depends(get_db),
    user_id: id = Depends(get_user_id),
):
    return await SubtasksService.create_subtask(task_id, subtask_data, db, user_id)


@router.get('/tasks/{task_id}', response_model=GetSubtasksResponse)
async def get_subtasks_by_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    return await SubtasksService.get_subtasks_by_task(task_id, db, user_id)

@router.patch('/{subtask_id}', response_model=UpdateSubtaskResponse)
async def update_subtask(
    subtask_id: int,
    subtask_data: UpdateSubtaskRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    return await SubtasksService.update_subtask(subtask_id, subtask_data, db, user_id)

@router.delete('/{subtask_id}')
async def delete_subtask(
    subtask_id: int, 
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    await SubtasksService.delete_subtask(subtask_id, db, user_id)

