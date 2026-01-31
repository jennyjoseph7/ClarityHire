import os
import uuid
import shutil
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.api import deps
from app.models.resume import Resume, ResumeStatus
from app.worker import parse_resume_task

router = APIRouter()

# Determine absolute path for uploads directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        safe_filename = f"{file_id}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        
        # Read content to get size and then write
        content = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        file_size = len(content)
        
        resume = Resume(
            id=uuid.UUID(file_id),
            user_id=current_user.id,
            original_filename=file.filename,
            file_path=file_path,
            file_size_bytes=file_size,
            status=ResumeStatus.PENDING
        )
        
        db.add(resume)
        await db.commit()
        await db.refresh(resume)
        
        # Trigger Celery Task (Pass absolute path for safety)
        print(f"DEBUG: Dispatching Resume {resume.id} to Celery via {file_path}")
        try:
            task = parse_resume_task.delay(str(resume.id), file_path)
            print(f"DEBUG: Dispatch SUCCESS! Task ID: {task.id}")
        except Exception as celery_err:
            print(f"CELERY TASK DISPATCH FAILED: {celery_err}")
            import traceback
            traceback.print_exc()
        
        # Return a dict to avoid serialization issues with SQLAlchemy objects
        return {
            "id": str(resume.id),
            "status": resume.status,
            "filename": resume.original_filename
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"CRITICAL UPLOAD ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.get("/mine", response_model=List[dict])
async def get_my_resumes(
    db: AsyncSession = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(select(Resume).where(Resume.user_id == current_user.id).order_by(desc(Resume.id)))
    return result.scalars().all()

@router.get("/mine/latest")
async def get_my_latest_resume(
    db: AsyncSession = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(
        select(Resume)
        .where(Resume.user_id == current_user.id, Resume.status == ResumeStatus.PARSED)
        .order_by(desc(Resume.id))
        .limit(1)
    )
    resume = result.scalars().first()
    if not resume:
        return {"id": None}
    return resume

@router.get("/{resume_id}")
async def get_resume_status(
    resume_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    resume = await db.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return resume
