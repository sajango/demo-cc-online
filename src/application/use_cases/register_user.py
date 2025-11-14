from injector import inject
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.services.password_service import PasswordService


class RegisterUserUseCase:
    """Use case for registering a new user"""

    @inject
    def __init__(self, user_repository: UserRepository, password_service: PasswordService):
        self.user_repository = user_repository
        self.password_service = password_service

    async def execute(self, email: str, username: str, full_name: str, password: str) -> User:
        """
        Register a new user with local authentication

        Args:
            email: User email
            username: User username
            full_name: User full name
            password: Plain text password

        Returns:
            Created user entity

        Raises:
            ValueError: If user with email already exists
        """
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError(f"User with email {email} already exists")

        # Hash the password
        password_hash = self.password_service.hash_password(password)

        # Create new user entity
        user = User(
            email=email,
            username=username,
            full_name=full_name,
            password_hash=password_hash,
            auth_provider="local",
            is_active=True,
            is_verified=False,
        )

        # Save to repository
        return await self.user_repository.create(user)
