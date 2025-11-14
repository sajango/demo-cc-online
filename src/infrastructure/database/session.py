from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool
from src.core.config import settings

# Create async engine
engine = None
async_session_factory = None


def get_async_engine():
    """Get or create async database engine"""
    global engine
    if engine is None:
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DB_ECHO,
            poolclass=NullPool,
            future=True,
        )
    return engine


def get_async_session_factory(engine=None):
    """Get or create async session factory"""
    global async_session_factory
    if async_session_factory is None:
        if engine is None:
            engine = get_async_engine()
        async_session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return async_session_factory


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session
    """
    factory = get_async_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
