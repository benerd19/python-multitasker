from .schemas import (
    CreateCategoryRequest,
    UpdateCategoryRequest,
)
from sqlalchemy.ext.asyncio import AsyncSession
from .models import ActivityCategoriesTable
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.exceptions import NotFoundError

class CategoriesService:

    @staticmethod
    async def create_category(
        category_data: CreateCategoryRequest,
        user_id: int,
        db: AsyncSession
    ):
        new_category = ActivityCategoriesTable(
            **category_data.model_dump(), user_id=user_id
        )
        
        db.add(new_category)
        
        await db.commit()
        await db.refresh(new_category)
        
        return new_category

    @staticmethod
    async def get_users_categories(
        user_id: int,
        db: AsyncSession
    ):
        result = await db.execute(
            select(ActivityCategoriesTable)
            .where(ActivityCategoriesTable.user_id == user_id)
            .options(selectinload(ActivityCategoriesTable.projects)))
        
        categories = result.scalars().all()
        
        if not categories:
            raise NotFoundError('Категории не найдены')
        return categories

    @staticmethod
    async def get_category(
        category_id: int,
        user_id: int,
        db: AsyncSession
    ):
        result = await db.execute(select(ActivityCategoriesTable).where(
                ActivityCategoriesTable.id == category_id,
                ActivityCategoriesTable.user_id == user_id
            ))
        
        category = result.scalar_one_or_none()
        
        if (category is None):
            raise NotFoundError('Категория не найдена')
        
        return category

    @staticmethod
    async def update_category(
        category_id: int,
        category_data: UpdateCategoryRequest,
        user_id: int,
        db: AsyncSession
    ):
        result = await db.execute(select(ActivityCategoriesTable).where(
                ActivityCategoriesTable.id == category_id,
                ActivityCategoriesTable.user_id == user_id
                ))
        
        category = result.scalar_one_or_none()
        
        if (category is None):
            raise NotFoundError('Категория не найдена')
        
        updated_data = category_data.model_dump(exclude_unset=True)
        
        for field, value in updated_data.items():
            setattr(category, field, value)
        
        await db.commit()
        await db.refresh(category)
        
        return category

    @staticmethod
    async def delete_category(
        category_id: int,
        user_id: int,
        db: AsyncSession
    ):
        result = await db.execute(select(ActivityCategoriesTable).where(
                ActivityCategoriesTable.id == category_id,
                ActivityCategoriesTable.user_id == user_id
            ))
        
        category = result.scalar_one_or_none()
        
        if (category is None):
            raise NotFoundError('Категория не найдена')
        
        await db.delete(category)
        await db.commit()
        
        return None