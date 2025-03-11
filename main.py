from fastapi import FastAPI, HTTPException
from schemas import Belts, BJJUser


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
    {"id": 3, "name": "DanVP", "belt": "blue", "gym": "Maven", "strengths": [
        {"area": "wrestling"},
        {"area": "butterfly guard"},
    ]},
    {"id": 4, "name": "Chris", "belt": "white", "gym": "Maven", "strengths": []}
]


# Method to get all users
@app.get("/users")
async def users(belt: Belts | None = None) -> list[BJJUser]:
    if belt:
        return [
            BJJUser(**user) for user in USERS if user['belt'] == belt.value
        ]
    return [BJJUser(**user) for user in USERS]

# Method to get a user by user_id
@app.get("/user/{user_id}")
async def user(user_id: int) -> BJJUser:
    user = next((BJJUser(**user) for user in USERS if user['id'] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

# Method to get all users by belt level
@app.get("/users/belt/{belt}")
async def get_users_by_belt(belt: Belts) -> list[BJJUser]:
    # Add handling if no results returned
    return [BJJUser(**user) for user in USERS if user['belt'] == belt.value]


# Method to get user by user name
# Method to get user by strengths
# Method to get user by gym