import asyncio
from app.db.session import AsyncSessionLocal
from app.models.resume import Resume
from sqlalchemy import select, desc

async def check_resumes():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Resume).order_by(desc(Resume.id)).limit(5))
        resumes = result.scalars().all()
        
        if not resumes:
            print("No resumes found in database")
        else:
            print(f"\n{'='*80}")
            print(f"Found {len(resumes)} resume(s) in database:")
            print(f"{'='*80}\n")
            
            for r in resumes:
                print(f"Resume ID: {r.id}")
                print(f"Filename: {r.original_filename}")
                print(f"Status: {r.status}")
                print(f"File Path: {r.file_path}")
                if r.error_message:
                    print(f"❌ Error: {r.error_message}")
                if r.parsed_json:
                    import json
                    print(f"✅ Parsed Data: {json.dumps(r.parsed_json, indent=2)[:200]}...")
                print(f"{'-'*80}\n")

asyncio.run(check_resumes())
