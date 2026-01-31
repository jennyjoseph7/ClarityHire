import asyncio
import asyncpg
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

print(f"Asyncpg Version: {asyncpg.__version__}")
print(f"Asyncpg Path: {asyncpg.__file__}")

# Add backend to path to import app
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.core.config import settings

async def test_connection():
    url = settings.DATABASE_URL
    print(f"Testing connection to: {url.split('@')[1] if '@' in url else 'LOCAL'}")
    print(f"Full URL (masked): {url.replace(url.split(':')[2].split('@')[0], '******') if '@' in url else url}")
    
    import ssl
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    
    try:
        engine = create_async_engine(url, connect_args={"ssl": ssl_ctx})
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print(f"Success! Result: {result.scalar()}")
    except Exception as e:
        print(f"Connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_connection())
