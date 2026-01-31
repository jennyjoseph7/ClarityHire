from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID

class JobBase(BaseModel):
    title: str
    description: str
    company: str
    location: Optional[str] = "Remote"

class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    title: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None

class JobInDBBase(JobBase):
    id: UUID
    posted_by: UUID
    parsed_requirements: Optional[dict] = None

    class Config:
        from_attributes = True

class Job(JobInDBBase):
    pass
