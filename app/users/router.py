import asyncio

from sqlalchemy import select, delete
from app.core.deps import get_user_id
from app.database import get_db
from fastapi import APIRouter, HTTPException, Request, Response, Depends, status
from app.core.security import create_tokens, decode_token, hash_password, verify_password
from app.users.schemas import (
    UsersCreateRequest, 
    UsersCreateResponse, 
    UsersGetInfoResponse, 
    UsersAuthRequest, 
    UsersAuthResponse, 
    UsersPartialUpdate)
from .models import UsersTable
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/users', tags=['Users'])

#USERS
@router.post('/',  response_model=UsersCreateResponse)
async def create_user(response: Response, user: UsersCreateRequest, db: AsyncSession = Depends(get_db)):
    hashed_password = await asyncio.to_thread(hash_password, user.password)
    
    user_data = user.model_dump()
    user_data['password'] = hashed_password

    new_user = UsersTable(**user_data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    refresh, access = create_tokens({"user_id":new_user.id})

    response.set_cookie(
        key='refresh_token',
        value=refresh,
        httponly=True
    )
    return {"access": access}

@router.get('/me', response_model=UsersGetInfoResponse)
async def get_user_info(
    user_id: int = Depends(get_user_id), 
    db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(UsersTable).where(UsersTable.id == user_id))

    user_info = result.scalars().first()

    if user_info is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user_info

@router.post('/auth', response_model=UsersAuthResponse)
async def authenticate_user(
    user: UsersAuthRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UsersTable).where(user.email == UsersTable.email))

    found_user = result.scalars().first()

    if (found_user is None): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    is_valid = await asyncio.to_thread(verify_password, found_user.password, user.password)

    if (not is_valid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    access, refresh = create_tokens({"user_id": found_user.id})

    response.set_cookie(
        key='refresh_token',
        value=refresh,
        httponly=True
    )

    return {"access" : access}

@router.post('/tokens/refresh', response_model=UsersAuthResponse)
async def refresh_tokens(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    refresh_token = request.cookies.get('refresh_token')

    if (refresh_token is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    payload = decode_token(refresh_token)

    if (payload is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_id = payload.get("user_id")

    if (user_id is None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    result = await db.execute(select(UsersTable).where(UsersTable.id == user_id))

    user = result.scalar_one_or_none()

    if (user is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    access, refresh = create_tokens({"user_id": user.id})

    response.set_cookie(
        key = "refresh_token",
        value=refresh,
        httponly=True
    )

    return {"access": access}

@router.patch('/', response_model=UsersPartialUpdate)
async def update_user(
    updated_data: UsersPartialUpdate,
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UsersTable).select(UsersTable.id == user_id))

    user = result.scalar_one_or_none()

    if (user is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    updated_user = updated_data.model_dump(exclude_unset=True)

    for field, value in updated_user.items():
        setattr(user, field, value)    

    await db.commit()

    return user

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(delete(UsersTable).where(UsersTable.id == user_id))
    
    if (result.rowcount == 0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await db.commit()

    
    return None
    