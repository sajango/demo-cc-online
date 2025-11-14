from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from src.infrastructure.database.session import get_session
from src.infrastructure.cache.redis_client import get_redis


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting database session
    """
    async for session in get_session():
        yield session


async def get_cache() -> AsyncGenerator[Redis, None]:
    """
    Dependency for getting Redis cache client
    """
    async for redis in get_redis():
        yield redis
