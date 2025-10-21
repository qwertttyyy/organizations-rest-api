from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from app.config import settings

DATABASE_URL = settings.get_database_url()

engine = create_async_engine(
    DATABASE_URL, echo=settings.DEBUG, future=True, pool_pre_ping=True
)
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор сессии базы данных."""
    async with AsyncSessionLocal() as session:
        yield session
