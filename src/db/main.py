from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config

engine = AsyncEngine(
    create_engine(
    url="postgresql+asyncpg://neondb_owner:npg_wOlBQ0oZPeT2@ep-long-resonance-abk64k7e-pooler.eu-west-2.aws.neon.tech/neondb",
    echo=True
    ))


async def init_db():
    async with engine.begin() as conn:
        statement = text("SELECT 'Hello';")
        result = await conn.execute(statement)

        print(result.all())