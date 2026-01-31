from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from app.api import deps
from app.models.job import Job
from app.core.config import settings
from groq import Groq
import json

router = APIRouter()

async def analyze_job_description(description: str) -> dict:
    """
    Use LLM to extract structured requirements from a job description.
    """
    client = Groq(api_key=settings.GROQ_API_KEY)
    
    prompt = f"""
    You are an expert Job Analyzer. Extract structured requirements from the job description text below and return ONLY valid JSON.
    Do not add any markdown formatting or explanations.
    
    Structure:
    {{
        "required_skills": [],
        "preferred_skills": [],
        "experience_years": 0,
        "education_level": "",
        "key_responsibilities": []
    }}
    
    Job Description:
    {description[:10000]}
    """
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"}
    )
    
    return json.loads(completion.choices[0].message.content)

from app.schemas.job import JobCreate

@router.post("/", response_model=dict)
async def create_job(
    *,
    db: AsyncSession = Depends(deps.get_db),
    job_in: JobCreate,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new job posting and analyze it.
    """
    # 1. Analyze with LLM
    try:
        structured_requirements = await analyze_job_description(job_in.description)
    except Exception as e:
        structured_requirements = {"error": str(e)}

    # 2. Create Job Record
    db_job = Job(
        title=job_in.title,
        description=job_in.description,
        company=job_in.company,
        location=job_in.location,
        posted_by=current_user.id,
        parsed_requirements=structured_requirements
    )
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)

    return db_job

@router.get("/", response_model=List[dict])
async def list_jobs(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve jobs.
    """
    result = await db.execute(select(Job).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{id}", response_model=dict)
async def get_job(
    id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Get job by ID.
    """
    job = await db.get(Job, id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return job
