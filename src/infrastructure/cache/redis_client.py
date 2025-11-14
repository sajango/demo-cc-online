from typing import AsyncGenerator, Optional
from redis.asyncio import Redis, from_url
from src.core.config import settings

redis_client: Optional[Redis] = None


def get_redis_client() -> Redis:
    """Get or create Redis client"""
    global redis_client
    if redis_client is None:
        redis_client = from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    return redis_client


async def get_redis() -> AsyncGenerator[Redis, None]:
    """
    Dependency for getting Redis client
    """
    client = get_redis_client()
    try:
        yield client
    finally:
        # Redis client is managed globally, no need to close here
        pass


async def close_redis():
    """Close Redis connection"""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
