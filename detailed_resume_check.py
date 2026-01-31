"""Check if resume was uploaded and trace the issue"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import asyncio
from sqlalchemy import select, desc, func
from app.db.session import AsyncSessionLocal
from app.models.resume import Resume

async def main():
    async with AsyncSessionLocal() as db:
        # Count total resumes
        count_result = await db.execute(select(func.count()).select_from(Resume))
        total = count_result.scalar()
        
        print(f"Total resumes in database: {total}")
        
        if total == 0:
            print("\nNO RESUMES FOUND!")
            print("The upload API endpoint is likely failing.")
            print("Check the FastAPI server logs for errors.")
            return
        
        # Get latest resumes
        result = await db.execute(
            select(Resume).order_by(desc(Resume.created_at)).limit(3)
        )
        resumes = result.scalars().all()
        
        print(f"\n{'='*70}")
        print("LATEST RESUMES:")
        print('='*70)
        
        for r in resumes:
            print(f"\nID: {r.id}")
            print(f"Filename: {r.original_filename}")
            print(f"Status: {r.status}")
            print(f"File path: {r.file_path}")
            print(f"Created: {r.created_at}")
            
            # Check if file exists
            if os.path.exists(r.file_path):
                print(f"File exists: YES (size: {os.path.getsize(r.file_path)} bytes)")
            else:
                print(f"File exists: NO - FILE MISSING!")
            
            if r.error_message:
                print(f"ERROR: {r.error_message}")
            
            if r.parsed_json:
                print("Parsed data: YES")
                import json
                print(json.dumps(r.parsed_json, indent=2)[:300])
            else:
                print("Parsed data: NO")
            
            print('-'*70)

try:
    asyncio.run(main())
except Exception as e:
    print(f"Database error: {e}")
    import traceback
    traceback.print_exc()
