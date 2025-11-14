from typing import Dict
from injector import inject
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.services.jwt_service import JWTService


class RefreshTokenUseCase:
    """Use case for refreshing access token"""

    @inject
    def __init__(self, user_repository: UserRepository, jwt_service: JWTService):
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    async def execute(self, refresh_token: str) -> Dict[str, str]:
        """
        Generate new access token from refresh token

        Args:
            refresh_token: Valid refresh token

        Returns:
            Dictionary with new access_token and refresh_token

        Raises:
            ValueError: If refresh token is invalid
        """
        # Verify refresh token
        payload = self.jwt_service.verify_token(refresh_token, token_type="refresh")
        if not payload:
            raise ValueError("Invalid or expired refresh token")

        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Invalid token payload")

        # Get user by ID
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Check if user is active
        if not user.is_active:
            raise ValueError("Account is deactivated")

        # Generate new tokens
        token_data = {"sub": user.id, "email": user.email, "username": user.username}

        access_token = self.jwt_service.create_access_token(token_data)
        new_refresh_token = self.jwt_service.create_refresh_token({"sub": user.id})

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }
