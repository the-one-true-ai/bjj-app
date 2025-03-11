from fastapi import FastAPI, HTTPException
from schemas import Belts, UserBase, UserCreate, UserWithID


app = FastAPI()

USERS = [
    {"id": 1, "name": "Adam", "belt": "black", "gym": "DPG", "strengths": [
        {"area": "leg locks"},
        {"area": "mobility"},
        {"area": "inversion"},
    ]},
    {"id": 2, "name": "Achal", "belt": "blue", "gym": "Maven", "strengths": [
        {"area": "DLR"},
        {"area": "halfguard"},
    ]},
    {"id": 3, "name": "DanVP", "belt": "blue", "gym": "Maven", "strengths": []},
    {"id": 4, "name": "Chris", "belt": "white", "gym": "Maven", "strengths": []}
]



# Method to create a user
@app.post("/users")
async def create_user(user_data: UserCreate) -> UserWithID:
    print(user_data)  # Log the incoming data for debugging
    new_id = USERS[-1]['id'] + 1
    new_user = UserWithID(id=new_id, **user_data.dict())
    USERS.append(new_user.dict())
    return new_user


# Method to get all users, optional query parameter of belt added
@app.get("/users")
async def users(
    belt: Belts | None = None,
    has_strengths: bool | None = None
    ) -> list[UserWithID]:
    
    user_list = [UserWithID(**user) for user in USERS]

    # Filtering by belt
    if belt:
        user_list = [
            user for user in user_list if user.belt == belt.value
        ]
    
    # Filtering by strengths
    if has_strengths == True:
        user_list = [
            user for user in user_list if len(user.strengths) > 0
        ]
    elif has_strengths == False:
        user_list = [
            user for user in user_list if len(user.strengths) <= 0
        ]
    else:
        user_list = user_list

    # Return
    return user_list

# Method to get a user by user_id
@app.get("/user/{user_id}")
async def user(user_id: int) -> UserWithID:
    user = next((UserWithID(**user) for user in USERS if user['id'] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


