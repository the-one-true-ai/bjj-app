from typing import Optional, List
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

# FastAPI app
app = FastAPI()

class User(BaseModel):
    id: int
    name: str

class UserUpdateModel(User):
    name: str


# Database
USERS_DATA = [
    {"id":1, "name":"Achal Inamdar"},
    {"id":2, "name":"Dan Van Pelt"},
    {"id":3, "name":"Adam Ellis"},
    {"id":4, "name":"Dan Geoghagen"},
    {"id":5, "name":"Gordon Ryan"}
]

@app.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_all_users():
    return USERS_DATA

@app.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_a_user(user_id:int):
    for user in USERS_DATA:
        if user_id == user['id']:
            return user        
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find a user with ID:{user_id}.")

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_a_user(user_data:User):
    new_user = user_data.model_dump()
    USERS_DATA.append(new_user)
    return new_user


@app.patch("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_a_user(user_id:int, user_update_data: UserUpdateModel) -> dict:
    for user in USERS_DATA:
        if user_id == user['id']:
            user['name'] = user_update_data.name
            return user
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find a user with ID:{user_id} to update.")        

@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_a_user(user_id:int):
    for user in USERS_DATA:
        if user_id == user['id']:
            USERS_DATA.remove(user)
            return {}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find a user with ID:{user_id} to delete.")            