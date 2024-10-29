from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import ASYNC_DATABASE_URL, SYNC_DATABASE_URL

# Async engine and session
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

# Sync engine and session
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Base model for ORM
Base = declarative_base()

# Async database session dependency
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session

# Sync database session dependency
def get_sync_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
