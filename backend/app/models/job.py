import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class JobStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING_ANALYSIS = "pending_analysis"
    ACTIVE = "active"
    CLOSED = "closed"

class Job(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recruiter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    raw_description = Column(Text, nullable=False)
    parsed_json = Column(JSONB, nullable=True)
    quality_score = Column(Integer, nullable=True)
    status = Column(Enum(JobStatus), default=JobStatus.DRAFT, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    analyzed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    closes_at = Column(TIMESTAMP(timezone=True), nullable=True)
    
    # Relationships
    recruiter = relationship("User", backref="jobs")
