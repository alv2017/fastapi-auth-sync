from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from api.config import settings


def _get_async_engine() -> AsyncEngine:
    engine: AsyncEngine = create_async_engine(
        settings.db.url,
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
    )
    return engine


db_engine = _get_async_engine()

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=db_engine,
    class_=AsyncSession,
)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session
