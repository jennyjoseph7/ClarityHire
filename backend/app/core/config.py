from pydantic_settings import BaseSettings
from typing import Optional, Any
from pydantic import field_validator, ValidationInfo
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "ClarityHire"
    API_V1_STR: str = "/api/v1"
    
    # Database
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: Optional[str] = None
    DATABASE_URL: Optional[str] = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            if v.startswith("postgres://"):
                v = v.replace("postgres://", "postgresql+asyncpg://", 1)
            elif v.startswith("postgresql://"):
                v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
            
            # Explicitly strip sslmode/ssl from URL to avoid SQLAlchemy auto-adding channel_binding
            if "sslmode=require" in v:
                v = v.replace("?sslmode=require", "").replace("&sslmode=require", "")
            if "ssl=require" in v:
                v = v.replace("?ssl=require", "").replace("&ssl=require", "")
            
            # Also strip channel_binding which causes issues with asyncpg on Windows
            if "channel_binding=" in v:
                 v = v.split("channel_binding=")[0].rstrip("?&")
            
            return v
        
        # Fallback if not provided in env
        values = info.data
        if values.get("POSTGRES_USER") and values.get("POSTGRES_SERVER"):
             return f"postgresql+asyncpg://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}"
        return None
    
    # Redis
    REDIS_HOST: Optional[str] = "localhost"
    REDIS_PORT: str = "6379"
    REDIS_URL: Optional[str] = None

    @field_validator("REDIS_URL", mode="before")
    @classmethod
    def assemble_redis_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            # Clean up if user pasted redis-cli command
            if "redis-cli" in v:
                parts = v.split()
                for p in parts:
                    if p.startswith("redis://") or p.startswith("rediss://"):
                        v = p
                        break
            
            # Standardize for Upstash/TLS
            if "upstash" in v or ":6379" in v:
                if v.startswith("redis://"):
                    v = v.replace("redis://", "rediss://", 1)
                
                # Add SSL params if missing for Windows/Upstash stability
                if "ssl_cert_reqs" not in v:
                    separator = "&" if "?" in v else "?"
                    v = f"{v}{separator}ssl_cert_reqs=none"
            
            return v
            
        # Fallback
        return None  # Will be handled by the field's default or another place
        
    def get_redis_url(self) -> str:
        if self.REDIS_URL:
            return self.REDIS_URL
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # LLM
    GROQ_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
# Override REDIS_URL if it's still None to provide the default
if not settings.REDIS_URL:
    settings.REDIS_URL = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
