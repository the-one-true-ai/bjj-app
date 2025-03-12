from fastapi import FastAPI
from src.users.routes import user_router

version = "v1"

app = FastAPI(
    title="BJJ App",
    description="A REST API for a sick BJJ App",
    version=version
)

app.include_router(router = user_router, prefix=f"/api/{version}/users", tags=["users"])
