from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

async_engine = AsyncEngine(
    create_engine(
    url=Config.DATABASE_URL,
    echo=True
    ))


async def init_db():
    async with async_engine.begin() as conn:
        from src.users.models import FactUser

        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession: # type: ignore
    Session = sessionmaker(
        bind = async_engine,
        class_ = AsyncSession,
        expire_on_commit = False
    )

    async with Session() as session:
        yield session