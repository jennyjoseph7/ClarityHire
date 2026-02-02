import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from sqlalchemy import text
from groq import Groq
from redis import Redis

async def verify_db():
    print(f"1. Testing Async DB Connection...")
    print(f"   URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'HIDDEN'}")
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            val = result.scalar()
            print(f"   ✅ DB Connection Successful! Result: {val}")
            return True
    except Exception as e:
        print(f"   ❌ DB Connection Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_groq():
    print(f"\n2. Testing Groq API...")
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Groq is ready' in JSON format: {'status': 'Groq is ready'}",
                }
            ],
            model="llama3-70b-8192",
            response_format={"type": "json_object"},
        )
        print(f"   ✅ Groq API Successful! Response: {chat_completion.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"   ❌ Groq API Failed: {e}")
        return False

def verify_redis():
    print(f"\n3. Testing Redis Connection...")
    try:
        # Use settings to get the cleaned URL
        redis_url = settings.get_redis_url()
        print(f"   URL: {redis_url[:20]}...")
        # We need to handle the SSL cert reqs manually if using redis-py directly with this URL string
        # Config.py does it for Celery/Settings, but here we just want a quick pong.
        # However, redis-py from URL should handle it.
        
        # Note: If config.py adds ssl_cert_reqs=none, it's a query param.
        r = Redis.from_url(redis_url)
        if r.ping():
             print(f"   ✅ Redis Ping Successful!")
             return True
    except Exception as e:
        print(f"   ❌ Redis Ping Failed: {e}")
        return False

async def main():
    print("=== Phase 1 System Verification ===\n")
    db_ok = await verify_db()
    groq_ok = verify_groq()
    redis_ok = verify_redis()
    
    print("\n=== Summary ===")
    print(f"Database: {'✅' if db_ok else '❌'}")
    print(f"Groq LLM: {'✅' if groq_ok else '❌'}")
    print(f"Redis:    {'✅' if redis_ok else '❌'}")
    
    if db_ok and groq_ok and redis_ok:
        print("\nAll systems GO! The issue is likely in the worker code structure or execution flow.")
    else:
        print("\nSystem configuration issues detected. Please fix before debugging code.")

if __name__ == "__main__":
    asyncio.run(main())
