import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.core.config import settings

print(f"DATABASE_URL: {settings.DATABASE_URL[:20]}...")
print(f"REDIS_URL: {settings.REDIS_URL[:50]}...")
