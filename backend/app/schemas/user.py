from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Literal
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserBase(BaseModel):
    model_config = ConfigDict(extra='forbid')
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: Literal["candidate", "recruiter"]

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: UUID
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str
