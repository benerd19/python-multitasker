from .schemas import (
    CreateSubtaskRequest,
    UpdateSubtaskRequest,
)
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .models import SubTasksTable
from sqlalchemy import select
class SubtasksService:

    @staticmethod
    async def create_subtask(
        task_id: int,
        subtask_data: CreateSubtaskRequest,
        db: AsyncSession,
        user_id: int
    ):
        subtask = SubTasksTable(
                {**subtask_data.model_dump(), "owner_id": user_id, "task_id": task_id}
            )
        
        db.add(subtask)
        await db.commit()
        await db.refresh(subtask)
        
        return subtask

    @staticmethod
    async def get_subtasks_by_task(
        task_id: int,
        db: AsyncSession,
        user_id: int
    ):
        result = await db.execute(select(SubTasksTable).where(
            SubTasksTable.task_id == task_id,
            SubTasksTable.owner_id == user_id
        )) 
        
        tasks = result.scalars().all()
        
        return tasks

    @staticmethod
    async def update_subtask(
        subtask_id: int,
        subtask_data: UpdateSubtaskRequest,
        db: AsyncSession,
        user_id: int
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

    @staticmethod
    async def delete_subtask(
        subtask_id: int,
        db: AsyncSession,
        user_id: int
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
