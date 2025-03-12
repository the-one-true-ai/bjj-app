from fastapi import APIRouter, status
from src.users.user_data import USERS_DATA
from src.users.schemas import User, UserUpdateModel
from typing import  List
from fastapi.exceptions import HTTPException


user_router = APIRouter()


@user_router.get("/", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_all_users():
    return USERS_DATA

@user_router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_a_user(user_id:int):
    for user in USERS_DATA:
        if user_id == user['id']:
            return user        
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find a user with ID:{user_id}.")

@user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_a_user(user_data:User):
    new_user = user_data.model_dump()
    USERS_DATA.append(new_user)
    return new_user

@user_router.patch("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_a_user(user_id:int, user_update_data: UserUpdateModel) -> dict:
    for user in USERS_DATA:
        if user_id == user['id']:
            user['name'] = user_update_data.name
            return user
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find a user with ID:{user_id} to update.")        

@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_a_user(user_id:int):
    for user in USERS_DATA:
        if user_id == user['id']:
            USERS_DATA.remove(user)
            return {}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find a user with ID:{user_id} to delete.")            
