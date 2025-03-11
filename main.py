from fastapi import FastAPI, HTTPException
from schemas import BeltLevels, BJJUser


app = FastAPI()

USERS = [
    {"id": 1, "name": "Adam Ellis", "belt": "black", "gym": "DPG"},
    {"id": 2, "name": "Achal", "belt": "blue", "gym": "Maven"},
    {"id": 3, "name": "DanVP", "belt": "blue", "gym": "Maven"},
    {"id": 4, "name": "ArmyChris", "belt": "white", "gym": "Maven"}
]

@app.get("/users")
async def users() -> list[BJJUser]:
    return [
        BJJUser(**user) for user in USERS
    ]

@app.get("/users/{user_id}")
async def user(user_id: int) -> BJJUser:
    user = next((BJJUser(**user) for user in USERS if user['id'] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user