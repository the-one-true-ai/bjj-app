from fastapi import FastAPI, HTTPException
from schemas import BeltLevels, BJJUser


app = FastAPI()

USERS = [
    {"id": 1, "name": "Adam", "belt": "black", "gym": "DPG", "strengths": [
        {"area": "leg locks"},
        {"area": "mobility"},
        {"area": "inversion"},
    ]},
    {"id": 2, "name": "Achal", "belt": "blue", "gym": "Maven", "strengths": [
        {"area": "pressure"},
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
async def users() -> list[BJJUser]:
    # Add handling if no results returned
    return [
        BJJUser(**user) for user in USERS
    ]

# Method to get a user by user_id
@app.get("/users/{user_id}")
async def user(user_id: int) -> BJJUser:
    user = next((BJJUser(**user) for user in USERS if user['id'] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

# Method to get all users by belt level
@app.get("/users/belt/{belt_level}")
async def user_belt(belt_level: BeltLevels) -> list[BJJUser]:
    # Add handling if no results returned
    return [BJJUser(**user) for user in USERS if user['belt'] == belt_level.value]

    
# Method to get user by user name
# Method to get user by strengths
# Method to get user by gym