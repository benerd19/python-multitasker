
from app.core.deps import get_user_id
from app.database import get_db
from fastapi import APIRouter, HTTPException, Request, Response, Depends, status
from app.users.schemas import (
    UsersCreateRequest, 
    UsersCreateResponse, 
    UsersGetInfoResponse, 
    UsersAuthRequest, 
    UsersAuthResponse, 
    UsersPartialUpdate)
from sqlalchemy.ext.asyncio import AsyncSession
from .service import UsersService


router = APIRouter(prefix='/users', tags=['Users'])

#USERS
@router.post('/',  response_model=UsersCreateResponse)
async def create_user(response: Response, user: UsersCreateRequest, db: AsyncSession = Depends(get_db)):

    refresh, access = await UsersService.create_user(user, db)

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
    
    return await UsersService.get_user_info(user_id, db)

@router.post('/auth', response_model=UsersAuthResponse)
async def authenticate_user(
    user: UsersAuthRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    access, refresh = await UsersService.auth_user(user, db)

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

    access, refresh = await UsersService.refresh_tokens(refresh_token, db)

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
    return await UsersService.update_user_info(updated_data, db, user_id)

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int = Depends(get_user_id),
    db: AsyncSession = Depends(get_db)
):
    
    await UsersService.delete_user(user_id, db)
    return None
    