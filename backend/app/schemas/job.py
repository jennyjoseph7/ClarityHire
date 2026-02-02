from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

class JobBase(BaseModel):
    model_config = ConfigDict(extra='forbid')
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    company: str = Field(..., min_length=1, max_length=100)
    location: Optional[str] = Field("Remote", max_length=100)

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
