from .schemas import (
    CreateTaskRequest,
    UpdateTask
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select
from app.projects.models import ProjectsTable
from .models import TasksTable
from app.core.exceptions import NotFoundError
class TasksService:

    @staticmethod
    async def create_task(
        task: CreateTaskRequest,
        user_id: int,
        db: AsyncSession
    ):
        result = await db.execute(select(ProjectsTable).where(ProjectsTable.id == task.project_id))
        
        project = result.scalar_one_or_none()
        
        if (project is None):
            raise NotFoundError('Проект не найден')
        
        new_task = TasksTable(
                **task.model_dump(), 
                owner_id=user_id
            )
        
        db.add(new_task)
        
        await db.commit()
        await db.refresh(new_task)

        return new_task

    @staticmethod
    async def get_tasks_by_project(
        project_id: int,
        user_id: int,
        db: AsyncSession,
        per_page: int,
        page: int
    ):
        offset = (per_page * (page - 1))
        
        result = await db.execute(
            select(TasksTable)
            .limit(per_page)
            .offset(offset)
            .where(
                TasksTable.project_id == project_id, 
                TasksTable.owner_id == user_id
                ))
        
        
        tasks = result.scalars().all()
        
        if not tasks:
            raise NotFoundError('Задачи не найдены')
            
        
        return tasks
        

    @staticmethod
    async def update_task(
        task_id: int,
        updated_info: UpdateTask,
        user_id: int,
        db: AsyncSession
    ):
        result = await db.execute(
            select(TasksTable)
            .where(
                TasksTable.id == task_id,
                TasksTable.owner_id == user_id
                ))
        
        task = result.scalar_one_or_none()
        
        if task is None:
            raise NotFoundError('Задача не найдена')
            
        updated_data = updated_info.model_dump(exclude_unset=True)
        
        for field, value in updated_data.items():
            setattr(task, field, value)
        
        await db.commit()
        await db.refresh(task)
        
        return task 

    @staticmethod
    async def delete_task(
        task_id: int,
        user_id: int,
        db: AsyncSession
    ):
        result = await db.execute(
            select(TasksTable)
            .where(
                TasksTable.id == task_id, 
                TasksTable.owner_id == user_id))
        
        task = result.scalar_one_or_none()
        
        if task is None:
                raise NotFoundError('Задача не найдена')
            
        await db.delete(task)
        await db.commit()

        return None
