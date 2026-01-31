import asyncio
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import ssl

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.core.config import settings

async def check_status():
    url = settings.DATABASE_URL
    # Standardize URL for asyncpg
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    
    try:
        engine = create_async_engine(url, connect_args={"ssl": ssl_ctx})
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT status, original_filename, error_message FROM resumes ORDER BY created_at DESC LIMIT 1"))
            row = result.fetchone()
            if row:
                print(f"File: {row[1]}")
                print(f"Status: {row[0]}")
                print(f"Error: {row[2]}")
            else:
                print("No resumes found.")
    except Exception as e:
        print(f"Check failed: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(check_status())
