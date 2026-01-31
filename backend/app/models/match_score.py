import uuid
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class MatchScore(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    score = Column(Integer, nullable=False)
    breakdown = Column(JSONB, nullable=True)
    explanation = Column(Text, nullable=True)
    computed_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relationships
    job = relationship("Job")
    candidate = relationship("User", foreign_keys=[candidate_id])
    resume = relationship("Resume")
