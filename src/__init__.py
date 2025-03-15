from fastapi import FastAPI
from src.users.routes import user_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"Server is starting ...")
    await init_db()
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
app.include_router(router = auth_router, prefix=f"/api/{version}/auth", tags=["auth"])