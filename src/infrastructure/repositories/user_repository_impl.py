from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from injector import inject

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database.models import UserModel


class UserRepositoryImpl(UserRepository):
    """Implementation of UserRepository using SQLAlchemy"""

    @inject
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: UserModel) -> User:
        """Convert SQLAlchemy model to domain entity"""
        return User(
            id=model.id,
            email=model.email,
            username=model.username,
            full_name=model.full_name,
            password_hash=model.password_hash,
            auth_provider=model.auth_provider.value if model.auth_provider else "local",
            oauth_provider_id=model.oauth_provider_id,
            is_active=model.is_active,
            is_verified=model.is_verified,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        """Convert domain entity to SQLAlchemy model"""
        from src.infrastructure.database.models import AuthProvider

        return UserModel(
            id=entity.id,
            email=entity.email,
            username=entity.username,
            full_name=entity.full_name,
            password_hash=entity.password_hash,
            auth_provider=(
                AuthProvider(entity.auth_provider) if entity.auth_provider else AuthProvider.LOCAL
            ),
            oauth_provider_id=entity.oauth_provider_id,
            is_active=entity.is_active,
            is_verified=entity.is_verified,
        )

    async def create(self, user: User) -> User:
        """Create a new user"""
        model = self._to_model(user)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        result = await self.session.execute(select(UserModel).offset(skip).limit(limit))
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def update(self, user: User) -> User:
        """Update user"""
        result = await self.session.execute(select(UserModel).where(UserModel.id == user.id))
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"User with id {user.id} not found")

        model.email = user.email
        model.username = user.username
        model.full_name = user.full_name
        model.password_hash = user.password_hash
        model.is_active = user.is_active
        model.is_verified = user.is_verified

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def delete(self, user_id: str) -> bool:
        """Delete user"""
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.delete(model)
        await self.session.flush()
        return True
