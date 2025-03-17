from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.users.schemas import UserBaseSchema, UserUpdateSchema,  UserResponseSchema
from src.users.service import UserService
from src.auth.dependencies import AccessTokenBearer

user_router = APIRouter()
user_service = UserService()
access_token_bearer = AccessTokenBearer()


@user_router.get("/", response_model=List[UserResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_users(session: AsyncSession = Depends(get_session), auth_user_details: dict = Depends(access_token_bearer)):
    users = await user_service.get_all_users(session)
    return users



@user_router.post("/", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_a_user(user_data: UserBaseSchema, session: AsyncSession = Depends(get_session), auth_user_details: dict = Depends(access_token_bearer)):
    new_user = await user_service.create_a_user(user_data, session=session)
    return new_user


@user_router.get("/{user_uid}", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
async def get_a_user(user_uid: str, session: AsyncSession = Depends(get_session), auth_user_details: dict = Depends(access_token_bearer)):
    user = await user_service.get_user_by_id(user_uid, session)
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find a user with ID:{user_uid}.")
    else:
        return user

@user_router.patch("/{user_uid}", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
async def update_a_user(user_uid: str, user_update_data: UserUpdateSchema, session: AsyncSession = Depends(get_session), auth_user_details: dict = Depends(access_token_bearer)):
    updated_user = await user_service.update_a_user(user_uid, user_update_data, session)

    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find a user with ID:{user_uid} to update.")        
    else:        
        return updated_user