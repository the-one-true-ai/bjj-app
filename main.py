from fastapi import FastAPI, HTTPException, Path, Query
from models import Belts, UserBase, UserCreate, UserWithID, GymBase, Gym
from typing import Annotated, get_type_hints

app = FastAPI()

USERS = [
    {"id": 1, "name": "Adam", "belt": "Black", "gym": {"head_coach": "Adam Ellis"}, "stripes": 4},
    {"id": 2, "name": "Achal", "belt": "Blue", "gym": {"head_coach": "Dan G"}, "stripes": 2},
    {"id": 3, "name": "DanVP", "belt": "Blue", "gym": {"head_coach": "Dan G"}, "stripes": 1},
    {"id": 4, "name": "Chris", "belt": "White", "gym": {"head_coach": "Dan G"}, "stripes": 0}
]




# Method to create a user
@app.post("/users")
async def create_user(user_data: UserCreate) -> UserWithID:
    print(user_data)  # Log the incoming data for debugging
    new_id = USERS[-1]['id'] + 1
    new_user = UserWithID(id=new_id, **user_data.model_dump()).model_dump()
    USERS.append(new_user)
    return new_user


# Method to get all users, optional query parameter of belt added
@app.get("/users")
async def users(
    belt: Belts | None = None,
    q: Annotated[str | None, Query(max_length=10)] = None
    ) -> list[UserWithID]:
    
    user_list = [UserWithID(**user) for user in USERS]

    # Filtering by belt
    if belt:
        user_list = [
            user for user in user_list if user.belt.value.lower() == belt.value
        ]

    if q:
        user_list = [
            user for user in user_list if q.lower() in user.name.lower()
        ]
    

    # Return
    return user_list

# Method to get a user by user_id
@app.get("/user/{user_id}")
async def user(user_id: Annotated[int, Path(title="The ID of the user.")]) -> UserWithID:
    user = next((UserWithID(**user) for user in USERS if user['id'] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


