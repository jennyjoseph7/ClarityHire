import fitz  # PyMuPDF
import json
import os
from sqlalchemy.orm import Session
from app.core.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.models.resume import Resume, ResumeStatus
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
    You are an expert Resume Parser. Extract the following information from the resume text below and return ONLY valid JSON.
    Do not add any markdown formatting or explanations.
    
    Structure:
    {{
        "contact_info": {{ "name": "", "email": "", "phone": "", "linkedin": "", "location": "" }},
        "summary": "",
        "skills": [],
        "education": [ {{ "institution": "", "degree": "", "year": "" }} ],
        "experience": [ {{ "company": "", "role": "", "duration": "", "description": "" }} ]
    }}
    
    Resume Text:
    {text[:20000]}
    """
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"}
    )
    
    return json.loads(completion.choices[0].message.content)

@celery_app.task(ack_late=True)
def parse_resume_task(resume_id: str, file_path: str):
    import asyncio
    
    # 1. Update status to PARSING
    asyncio.run(update_resume_status(resume_id, ResumeStatus.PARSING))
    
    try:
        # 2. Extract Text
        text = extract_text_from_pdf(file_path)
        
        # 3. LLM Extraction
        parsed_data = parse_with_llm(text)
        
        # 4. Save Success
        asyncio.run(update_resume_status(resume_id, ResumeStatus.PARSED, parsed_data=parsed_data))
        
    except Exception as e:
        # 5. Handle Failure
        asyncio.run(update_resume_status(resume_id, ResumeStatus.FAILED, error=str(e)))
