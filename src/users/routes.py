from fastapi import APIRouter, status, Depends
from src.users.user_data import USERS_DATA
from src.users.schemas import User, UserUpdateModel, UserCreateModel
from src.db.main import get_session
from typing import  List
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.users.service import UserService


user_router = APIRouter()
user_service = UserService()


@user_router.get("/", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_all_users(session:AsyncSession = Depends(get_session)):
    users = await user_service.get_all_users(session)
    return users

@user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_a_user(user_data: UserCreateModel, session:AsyncSession = Depends(get_session)) -> dict:
    new_user = await user_service.create_a_user(user_data, session=session)

@user_router.get("/{user_uid}", response_model=User, status_code=status.HTTP_200_OK)
async def get_a_user(user_uid:int, session:AsyncSession = Depends(get_session)):
    user = await user_service.get_a_user(user_uid, session)
    
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find a user with ID:{user_uid}.")


@user_router.patch("/{user_uid}", response_model=User, status_code=status.HTTP_200_OK)
async def update_a_user(user_uid:int, user_update_data: UserUpdateModel, session:AsyncSession = Depends(get_session)) -> dict:
    updated_book = await user_service.update_a_user(user_uid, session)

    if updated_book:
        return updated_book
    else:        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find a user with ID:{user_uid} to update.")        

@user_router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_user(user_uid:int,session:AsyncSession = Depends(get_session)):
    user_to_delete = await user_service.delete_a_user(user_uid, session)

    if user_to_delete:
        return user_to_delete
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find a user with ID:{user_uid} to delete.")            
