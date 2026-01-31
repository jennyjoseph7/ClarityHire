from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from app.api import deps
from app.models.resume import Resume, ResumeStatus
from app.models.job import Job
from app.models.match_score import MatchScore
from app.core.scoring import calculate_match_score

router = APIRouter()

@router.get("/job/{job_id}", response_model=List[dict])
async def get_matches_for_job(
    job_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all candidate matches for a specific job.
    """
    job = await db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check if user is the poster or an admin
    if job.posted_by != current_user.id:
         raise HTTPException(status_code=403, detail="Not enough permissions")

    # Fetch all PARSED resumes
    result = await db.execute(select(Resume).where(Resume.status == ResumeStatus.PARSED))
    resumes = result.scalars().all()
    
    matches = []
    for resume in resumes:
        # Calculate score (In a real app, we'd cache this in the MatchScore table)
        # We check Cache first
        cache_result = await db.execute(
            select(MatchScore).where(MatchScore.job_id == job_id, MatchScore.resume_id == resume.id)
        )
        match_record = cache_result.scalars().first()
        
        if not match_record:
            score_data = calculate_match_score(resume.parsed_json, job.parsed_requirements)
            match_record = MatchScore(
                job_id=job_id,
                candidate_id=resume.user_id,
                resume_id=resume.id,
                score=score_data["score"],
                breakdown=score_data["breakdown"]
            )
            db.add(match_record)
            await db.commit()
            await db.refresh(match_record)
        
        matches.append({
            "candidate_id": resume.user_id,
            "resume_id": resume.id,
            "candidate_name": resume.original_filename, # Placeholder for user name
            "score": match_record.score,
            "breakdown": match_record.breakdown
        })
        
    # Sort by score descending
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches

@router.get("/resume/{resume_id}", response_model=List[dict])
async def get_matches_for_resume(
    resume_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all job matches for a specific resume.
    """
    resume = await db.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if resume.status != ResumeStatus.PARSED:
        return [] # Or raise error

    # Fetch all jobs
    result = await db.execute(select(Job))
    jobs = result.scalars().all()
    
    matches = []
    for job in jobs:
        # Check Cache
        cache_result = await db.execute(
            select(MatchScore).where(MatchScore.job_id == job.id, MatchScore.resume_id == resume_id)
        )
        match_record = cache_result.scalars().first()
        
        if not match_record:
            score_data = calculate_match_score(resume.parsed_json, job.parsed_requirements)
            match_record = MatchScore(
                job_id=job.id,
                candidate_id=resume.user_id,
                resume_id=resume.id,
                score=score_data["score"],
                breakdown=score_data["breakdown"]
            )
            db.add(match_record)
            await db.commit()
            await db.refresh(match_record)
            
        matches.append({
            "job_id": job.id,
            "job_title": job.title,
            "company": job.company,
            "score": match_record.score,
            "breakdown": match_record.breakdown
        })
        
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches
