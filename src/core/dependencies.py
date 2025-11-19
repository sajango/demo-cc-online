from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from src.infrastructure.database.session import get_session
from src.infrastructure.cache.redis_client import get_redis
from src.infrastructure.services.image_processor import ImageProcessorService
from src.infrastructure.services.zai_service import ZaiService
from src.core.config import settings


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


def get_image_processor_service() -> ImageProcessorService:
    """
    Dependency for getting image processor service
    """
    return ImageProcessorService()


def get_zai_service() -> ZaiService:
    """
    Dependency for getting Z-AI service
    """
    return ZaiService(api_key=settings.ZAI_API_KEY, base_url=settings.ZAI_BASE_URL)
