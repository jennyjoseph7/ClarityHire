import asyncio
import asyncpg
import os
import sys

# Load env manually since we are bypassing app config for raw test
def load_env():
    with open('.env', 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, val = line.strip().split('=', 1)
                os.environ[key] = val

async def run():
    load_env()
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("No DATABASE_URL found")
        return

    # Fix schemes for asyncpg
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    # We strip the asyncpg driver part for raw asyncpg
    # Actually asyncpg expects postgresql://...
    
    # Handle SSL manually
    ssl_param = "require" if "sslmode=require" in db_url or "ssl=require" in db_url else None
    
    # Clean URL for asyncpg if it has query params it dislikes
    # But usually we just pass the DSN
    print(f"Connecting to: {db_url.split('@')[1] if '@' in db_url else '...'}")

    try:
        # Test if channel_binding is accepted
        conn = await asyncpg.connect(db_url, ssl=ssl_param, channel_binding='prefer')
        print("Successfully connected!")
        await conn.close()
    except Exception as e:
        print(f"Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run())
