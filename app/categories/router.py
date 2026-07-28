from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_user_id
from app.database import get_db

from .schemas import (
    CategoriesByUserResponse,
    CreateCategoryRequest,
    CreateCategoryResponse,
    GetCategoryResponse,
    UpdateCategoryRequest,
    UpdateCategoryResponse,
)
from .service import CategoriesService

router = APIRouter(prefix='/categories', tags=["Categories"])

@router.post('/', response_model=CreateCategoryResponse)
async def create_category(
    category_data: CreateCategoryRequest,
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    return await CategoriesService.create_category(category_data, user_id, db)


@router.get('/', response_model=list[CategoriesByUserResponse])
async def get_users_categories(
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    return await CategoriesService.get_users_categories(user_id, db)
    

@router.get('/{category_id}', response_model=GetCategoryResponse)
async def get_category(
    category_id: int,
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    return await CategoriesService.get_category(category_id, user_id, db)

@router.patch('/{category_id}', response_model=UpdateCategoryResponse)
async def update_category(
    category_id: int,
    category_data : UpdateCategoryRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    return await CategoriesService.update_category(category_id, category_data, user_id, db)
    

@router.delete('/{category_id}')
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    await CategoriesService.delete_category(category_id, user_id, db)

