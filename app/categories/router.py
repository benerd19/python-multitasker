from fastapi import APIRouter, HTTPException, Request, Response, Depends, status
from sqlalchemy import select, delete
from app.core.deps import get_user_id
from app.database import get_db
from .schemas import (
    CategoriesByUserResponse,
    CreateCategoryRequest,
    CreateCategoryResponse,
    GetCategoryResponse,
    UpdateCategoryRequest,
    UpdateCategoryResponse
)
from .models import ActivityCategoriesTable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

router = APIRouter(prefix='/categories', tags=["Categories"])

@router.post('/', response_model=CreateCategoryResponse)
async def create_category(
    category_data: CreateCategoryRequest,
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    new_category = ActivityCategoriesTable(
        **{**category_data.model_dump(), "user_id": user_id}
    )

    db.add(new_category)

    await db.commit()
    await db.refresh(new_category)

    return new_category


@router.get('/', response_model=list[CategoriesByUserResponse])
async def get_users_categories(
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ActivityCategoriesTable).where(ActivityCategoriesTable.user_id == user_id).options(selectinload(ActivityCategoriesTable.projects)))

    categories = result.scalars().all()


    return categories

@router.get('/{category_id}', response_model=GetCategoryResponse)
async def get_category(
    category_id: int,
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ActivityCategoriesTable).where(
        ActivityCategoriesTable.id == category_id,
        ActivityCategoriesTable.user_id == user_id
    ))

    category = result.scalar_one_or_none()

    if (category is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return category

@router.patch('/{category_id}', response_model=UpdateCategoryResponse)
async def update_category(
    category_id: int,
    category_data : UpdateCategoryRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    result = await db.execute(select(ActivityCategoriesTable).where(
        ActivityCategoriesTable.id == category_id,
        ActivityCategoriesTable.user_id == user_id
        ))

    category = result.scalar_one_or_none()

    if (category is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    updated_data = category_data.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(category, field, value)

    await db.commit()
    await db.refresh(category)

    return category

@router.delete('/{category_id}')
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    result = await db.execute(select(ActivityCategoriesTable).where(
        ActivityCategoriesTable.id == category_id,
        ActivityCategoriesTable.user_id == user_id
    ))

    category = result.scalar_one_or_none()

    if (category is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await db.delete(category)
    await db.commit()

    return None