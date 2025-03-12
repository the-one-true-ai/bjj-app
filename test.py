import asyncpg
import asyncio

async def test_connection():
    try:
        conn = await asyncpg.connect(
            "postgresql://neondb_owner:npg_wOlBQ0oZPeT2@ep-long-resonance-abk64k7e-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require"
        )
        print("Connected successfully!")
        await conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

asyncio.run(test_connection())
