from fastapi import FastAPI
from src.users.routes import user_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"Server is starting ...")
    yield
    print(f"Server has been stopped.")


version = "v1"


app = FastAPI(
    title="BJJ App",
    description="A REST API for a sick BJJ App",
    version=version,
    lifespan=life_span
)


app.include_router(router = user_router, prefix=f"/api/{version}/users", tags=["users"])