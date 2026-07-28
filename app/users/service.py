import asyncio

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenError, NotFoundError, UnauthorizedError
from app.core.security import (
    create_tokens,
    decode_token,
    hash_password,
    verify_password,
)
from app.users.schemas import UsersAuthRequest, UsersCreateRequest, UsersPartialUpdate

from .models import UsersTable


class UsersService:

    @staticmethod
    async def create_user(
        user: UsersCreateRequest,
        db: AsyncSession

    ):
        hashed_password = await asyncio.to_thread(hash_password, user.password)
            
        user_data = user.model_dump()
        user_data['password'] = hashed_password
        
        new_user = UsersTable(**user_data)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        refresh, access = create_tokens({"user_id":new_user.id})
        
        return refresh, access

    @staticmethod
    async def get_user_info(
        user_id: int,
        db: AsyncSession
    ):
        result = await db.execute(select(UsersTable).where(UsersTable.id == user_id))
        user_info = result.scalars().first()
        
        if user_info is None:
            raise NotFoundError('Пользователь не найден')
        
        return user_info


    @staticmethod
    async def auth_user(
        user: UsersAuthRequest,
        db: AsyncSession        
    ):
        result = await db.execute(select(UsersTable).where(user.email == UsersTable.email))
        
        found_user = result.scalars().first()
        
        if (found_user is None): 
            raise ForbiddenError()
            
        is_valid = await asyncio.to_thread(verify_password, found_user.password, user.password)
        
        if (not is_valid):
            raise ForbiddenError()
        
        access, refresh = create_tokens({"user_id": found_user.id})

        return access, refresh

    @staticmethod
    async def refresh_tokens(
        refresh_token: str,
        db: AsyncSession
    ):
        payload = decode_token(refresh_token)
        
        if (payload is None):
            raise UnauthorizedError()
            
        user_id = payload.get("user_id")
        
        if (user_id is None):
            raise UnauthorizedError()
            
        result = await db.execute(select(UsersTable).where(UsersTable.id == user_id))
        
        user = result.scalar_one_or_none()
        
        if (user is None):
            raise NotFoundError('Пользователь не найден')
            
        access, refresh = create_tokens({"user_id": user.id})
        
        return access, refresh

    @staticmethod
    async def update_user_info(
        updated_data: UsersPartialUpdate,
        db: AsyncSession,
        user_id: int
    ):
        result = await db.execute(select(UsersTable).select(UsersTable.id == user_id))
        
        user = result.scalar_one_or_none()
        
        if (user is None):
            raise NotFoundError('Пользователь не найден')
        
        updated_user = updated_data.model_dump(exclude_unset=True)
        
        for field, value in updated_user.items():
            setattr(user, field, value)    
        
        await db.commit()
        
        return user

    @staticmethod
    async def delete_user(
        user_id: int,
        db: AsyncSession
    ):
        result = await db.execute(delete(UsersTable).where(UsersTable.id == user_id))
            
        if (result.rowcount == 0):
            raise NotFoundError('Пользователь не найден')

        await db.commit()

        



