from typing import Optional, List
from injector import inject
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository


class GetUserUseCase:
    """Use case for retrieving users"""

    @inject
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID

        Args:
            user_id: User ID

        Returns:
            User entity if found, None otherwise
        """
        return await self.user_repository.get_by_id(user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email

        Args:
            email: User email

        Returns:
            User entity if found, None otherwise
        """
        return await self.user_repository.get_by_email(email)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users with pagination

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of user entities
        """
        return await self.user_repository.get_all(skip=skip, limit=limit)
