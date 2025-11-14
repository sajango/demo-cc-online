from typing import Dict
from injector import inject
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.services.password_service import PasswordService
from src.infrastructure.services.jwt_service import JWTService


class LoginUserUseCase:
    """Use case for user login"""

    @inject
    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
        jwt_service: JWTService
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        self.jwt_service = jwt_service

    async def execute(
        self,
        email: str,
        password: str
    ) -> Dict[str, str]:
        """
        Authenticate a user and generate tokens

        Args:
            email: User email
            password: Plain text password

        Returns:
            Dictionary with access_token and refresh_token

        Raises:
            ValueError: If credentials are invalid
        """
        # Get user by email
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")

        # Check if user uses local authentication
        if user.auth_provider != "local":
            raise ValueError(f"Please login with {user.auth_provider}")

        # Verify password
        if not user.password_hash or not self.password_service.verify_password(
            password, user.password_hash
        ):
            raise ValueError("Invalid credentials")

        # Check if user is active
        if not user.is_active:
            raise ValueError("Account is deactivated")

        # Generate tokens
        token_data = {
            "sub": user.id,
            "email": user.email,
            "username": user.username
        }

        access_token = self.jwt_service.create_access_token(token_data)
        refresh_token = self.jwt_service.create_refresh_token({"sub": user.id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
