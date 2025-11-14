from injector import Injector, Module, provider, singleton
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from redis.asyncio import Redis
from src.core.config import settings
from src.infrastructure.database.session import get_async_engine, get_async_session_factory
from src.infrastructure.cache.redis_client import get_redis_client


class DatabaseModule(Module):
    """Module for database dependencies"""

    @singleton
    @provider
    def provide_async_engine(self):
        return get_async_engine()

    @singleton
    @provider
    def provide_session_factory(self, engine) -> async_sessionmaker:
        return get_async_session_factory(engine)


class CacheModule(Module):
    """Module for cache dependencies"""

    @singleton
    @provider
    def provide_redis_client(self) -> Redis:
        return get_redis_client()


class RepositoryModule(Module):
    """Module for repository dependencies"""

    # Add repository bindings here as you create them
    pass


class UseCaseModule(Module):
    """Module for use case dependencies"""

    # Add use case bindings here as you create them
    pass


def create_container() -> Injector:
    """Create and configure the dependency injection container"""
    return Injector(
        [
            DatabaseModule(),
            CacheModule(),
            RepositoryModule(),
            UseCaseModule(),
        ]
    )
