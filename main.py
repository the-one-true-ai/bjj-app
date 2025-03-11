from fastapi import FastAPI, HTTPException
from schemas import BeltLevels, User


app = FastAPI()

USERS = [
    {"id": 1, "name": "Adam Ellis", "belt": "black", "gym": "DPG"},
    {"id": 2, "name": "Achal", "belt": "blue", "gym": "Maven"},
    {"id": 3, "name": "DanVP", "belt": "blue", "gym": "Maven"},
    {"id": 4, "name": "ArmyChris", "belt": "white", "gym": "Maven"}
]

@app.get("/users")
async def users() -> list[User]:
    return [
        User(**u) for u in USERS
    ]