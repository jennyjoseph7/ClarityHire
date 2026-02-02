import fitz  # PyMuPDF
import json
import os
from sqlalchemy.orm import Session
from app.core.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.models.resume import Resume, ResumeStatus
from app.models.user import User  # Essential for SQLAlchemy relationship resolution
from app.core.config import settings
from groq import Groq
import asyncio

# Synchronous wrapper for database update because Celery runs in a separate thread/process
# Ideally we use async with Celery but for simplicity in this setup we might need a sync DB session adapter
# However, our DB stack is async.
# We will run the DB update part in a sync wrapper or using asyncio.run

async def update_resume_status(resume_id: str, status: ResumeStatus, parsed_data: dict = None, error: str = None):
    async with AsyncSessionLocal() as session:
        import uuid
        resume = await session.get(Resume, uuid.UUID(resume_id))
        if resume:
            resume.status = status
            if parsed_data:
                resume.parsed_json = parsed_data
            if error:
                resume.error_message = error
            await session.commit()

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def parse_with_llm(text: str) -> dict:
    client = Groq(api_key=settings.GROQ_API_KEY)
    
    prompt = f"""
You are an expert Resume Parser for a hiring intelligence platform. Extract ALL information from the resume text below and return ONLY valid JSON.

CRITICAL: This JSON will be used for skill-based matching, so extract:
1. Every skill mentioned (technical AND soft skills)
2. Evidence for each skill (where it was used: project, job, course, certification)
3. Quantify experience duration for each skill when possible
4. Extract projects with technologies used
5. Identify experience level indicators (fresher, junior, mid, senior)

Return this EXACT structure:
{{
    "name": "string",
    "email": "string",
    "phone": "string (optional)",
    "linkedin": "string (optional)",
    "location": "string",
    
    "skills": [
        {{
            "skill": "canonical name (e.g., React, Python, JavaScript)",
            "evidence": ["project:MindWell", "internship:Accenture", "certification:AWS"],
            "months_experience": "integer (estimate if not explicit, 0 if just learned)",
            "proficiency": "beginner|intermediate|advanced (infer from usage)"
        }}
    ],
    
    "projects": [
        {{
            "title": "string",
            "description": "string",
            "technologies": ["skill1", "skill2"],
            "duration": "string (e.g., '2 months', 'Dec 2025')",
            "key_achievements": ["string"],
            "url": "string (if mentioned)"
        }}
    ],
    
    "experience": [
        {{
            "company": "string",
            "role": "string",
            "type": "full-time|internship|virtual|contract",
            "start_date": "string (MMM YYYY)",
            "end_date": "string (MMM YYYY or 'Present')",
            "duration_months": "integer (calculate from dates)",
            "description": "string",
            "key_responsibilities": ["string"],
            "technologies_used": ["skill1", "skill2"]
        }}
    ],
    
    "education": [
        {{
            "institution": "string",
            "degree": "string (full name)",
            "field_of_study": "string",
            "start_date": "string",
            "end_date": "string",
            "year": "integer (graduation year)",
            "gpa": "string (if mentioned)",
            "relevant_coursework": ["string"]
        }}
    ],
    
    "certifications": [
        {{
            "name": "string",
            "issuer": "string",
            "date": "string (MMM YYYY)",
            "technologies": ["relevant skills"]
        }}
    ],
    
    "additional_info": {{
        "total_experience_months": "integer (sum of all work experience)",
        "experience_level": "fresher|junior|mid|senior (infer from total experience and roles)",
        "strongest_skills": ["top 5 skills based on evidence and usage"],
        "volunteering": ["string"],
        "languages": ["string (if mentioned)"]
    }}
}}

EXTRACTION RULES:
1. For skills: Extract EVERY technology, framework, library, tool, and methodology mentioned
2. For evidence: Link each skill to WHERE it was used (be specific: "project:MindWell" not just "project")
3. For duration: Calculate months from dates. If only year given, estimate reasonably
4. For proficiency: "advanced" if used in multiple contexts, "intermediate" if used in projects/work, "beginner" if only in courses
5. Normalize skill names: "React.js" → "React", "JS" → "JavaScript", "ML" → "Machine Learning"
6. Experience level logic:
   - 0-1 years + mostly virtual internships = "fresher"
   - 1-3 years + some real projects = "junior"
   - 3-5 years = "mid"
   - 5+ years = "senior"

Resume Text:
    {text[:20000]}
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"}
    )
    
    return json.loads(completion.choices[0].message.content)

async def parse_resume_async(resume_id: str, file_path: str):
    print(f"WORKER: Starting task for resume {resume_id}")
    try:
        # 1. Update status to PARSING
        print(f"WORKER: Updating status to PARSING...")
        await update_resume_status(resume_id, ResumeStatus.PARSING)
        
        # 2. Extract Text
        print(f"WORKER: Extracting text from {file_path}...")
        text = extract_text_from_pdf(file_path)
        print(f"WORKER: Extracted {len(text)} chars.")
        
        # 3. LLM Extraction (Sync call wrapped to avoid blocking loop too hard, though logic is simple)
        print(f"WORKER: Calling Groq LLM...")
        parsed_data = parse_with_llm(text)
        print(f"WORKER: LLM Success! Keys: {list(parsed_data.keys())}")
        
        # 4. Save Success
        print(f"WORKER: Saving results...")
        await update_resume_status(resume_id, ResumeStatus.PARSED, parsed_data=parsed_data)
        print(f"WORKER: Task Complete.")
        
    except Exception as e:
        print(f"WORKER ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        try:
            # 5. Handle Failure
            await update_resume_status(resume_id, ResumeStatus.FAILED, error=str(e))
        except Exception as db_err:
             print(f"WORKER CRITICAL: Check failed to update status to FAILED: {db_err}")

@celery_app.task(ack_late=True)
def parse_resume_task(resume_id: str, file_path: str):
    import asyncio
    try:
        asyncio.run(parse_resume_async(resume_id, file_path))
    except Exception as e:
        print(f"WORKER FATAL LOOP ERROR: {e}")
