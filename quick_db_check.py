import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import asyncio
from sqlalchemy import text
from app.db.session import engine

async def quick_check():
    async with engine.begin() as conn:
        # Check if resumes table has any data
        result = await conn.execute(text("""
            SELECT id, original_filename, status, error_message, created_at
            FROM resumes 
            ORDER BY created_at DESC 
            LIMIT 3
        """))
        
        rows = result.fetchall()
        
        if not rows:
            print("❌ NO RESUMES FOUND IN DATABASE")
            print("This means the upload never completed successfully.")
        else:
            print(f"\n✅ Found {len(rows)} resume(s):\n")
            for row in rows:
                print(f"ID: {row[0]}")
                print(f"Filename: {row[1]}")
                print(f"Status: {row[2]}")
                print(f"Error: {row[3] if row[3] else 'None'}")
                print(f"Created: {row[4]}")
                print("-" * 60)

try:
    asyncio.run(quick_check())
except Exception as e:
    print(f"❌ Database connection error: {e}")
