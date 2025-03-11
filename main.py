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
    {"id": 3, "name": "DanVP", "belt": "blue", "gym": "Maven", "strengths": []},
    {"id": 4, "name": "Chris", "belt": "white", "gym": "Maven", "strengths": []}
]


# Method to get all users, optional query parameter of belt added
@app.get("/users")
async def users(
    belt: Belts | None = None,
    has_strengths: bool = False
    ) -> list[BJJUser]:
    
    user_list = [BJJUser(**user) for user in USERS]

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
    else:
        user_list = [
            user for user in user_list if len(user.strengths) <= 0
        ]

    # Return
    return user_list
    
    

# Method to get a user by user_id
@app.get("/user/{user_id}")
async def user(user_id: int) -> BJJUser:
    user = next((BJJUser(**user) for user in USERS if user['id'] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


# Method to get user by user name
# Method to get user by strengths
# Method to get user by gym