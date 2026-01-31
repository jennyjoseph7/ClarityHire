import asyncio
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import ssl

# Add backend to path to import app
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.core.config import settings

async def check_columns():
    url = settings.DATABASE_URL
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    
    try:
        engine = create_async_engine(url, connect_args={"ssl": ssl_ctx})
        async with engine.connect() as conn:
            # Check for resumes table columns
            print("Checking 'resumes' table columns...")
            result = await conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'resumes'
            """))
            columns = [row[0] for row in result.fetchall()]
            print(f"Columns found: {columns}")
            
            if 'file_size_bytes' not in columns:
                print("MISSING: 'file_size_bytes' column!")
            else:
                print("FOUND: 'file_size_bytes' column.")
                
    except Exception as e:
        print(f"Check failed: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(check_columns())
