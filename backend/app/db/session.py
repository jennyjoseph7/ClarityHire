from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

import ssl

# Define SSL Context for AsyncPG
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# Pass connect_args to handle SSL without query params which confuse SQLAlchemy/AsyncPG
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True,
    connect_args={"ssl": ssl_ctx}
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
