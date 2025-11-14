from injector import inject
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository


class CreateUserUseCase:
    """Use case for creating a new user"""

    @inject
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(
        self,
        email: str,
        username: str,
        full_name: str
    ) -> User:
        """
        Create a new user

        Args:
            email: User email
            username: User username
            full_name: User full name

        Returns:
            Created user entity

        Raises:
            ValueError: If user with email already exists
        """
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError(f"User with email {email} already exists")

        # Create new user entity
        user = User(
            email=email,
            username=username,
            full_name=full_name,
            is_active=True
        )

        # Save to repository
        return await self.user_repository.create(user)
