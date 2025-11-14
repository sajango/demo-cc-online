from typing import Dict
from injector import inject
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.services.jwt_service import JWTService


class OAuthLoginUseCase:
    """Use case for OAuth login (Google, Apple)"""

    @inject
    def __init__(self, user_repository: UserRepository, jwt_service: JWTService):
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    async def execute(
        self, email: str, full_name: str, provider: str, provider_user_id: str
    ) -> Dict[str, str]:
        """
        Authenticate or register user via OAuth provider

        Args:
            email: User email from OAuth provider
            full_name: User full name from OAuth provider
            provider: OAuth provider name (google, apple)
            provider_user_id: User ID from OAuth provider

        Returns:
            Dictionary with access_token and refresh_token

        Raises:
            ValueError: If authentication fails
        """
        # Try to find existing user by email
        user = await self.user_repository.get_by_email(email)

        if user:
            # User exists
            # Check if auth provider matches
            if user.auth_provider != provider:
                raise ValueError(
                    f"Email already registered with {user.auth_provider}. "
                    f"Please login with {user.auth_provider}"
                )

            # Check if user is active
            if not user.is_active:
                raise ValueError("Account is deactivated")

            # Update OAuth provider ID if changed
            if user.oauth_provider_id != provider_user_id:
                user.oauth_provider_id = provider_user_id
                user = await self.user_repository.update(user)
        else:
            # Create new user from OAuth data
            username = email.split("@")[0]  # Generate username from email

            # Check if username exists, append numbers if needed
            counter = 1
            original_username = username
            while True:
                existing = await self.user_repository.get_by_email(f"{username}@temp")
                # Simple check, in production you'd have a get_by_username method
                if not existing:
                    break
                username = f"{original_username}{counter}"
                counter += 1

            user = User(
                email=email,
                username=username,
                full_name=full_name,
                password_hash=None,
                auth_provider=provider,
                oauth_provider_id=provider_user_id,
                is_active=True,
                is_verified=True,  # OAuth users are pre-verified
            )

            user = await self.user_repository.create(user)

        # Generate tokens
        token_data = {"sub": user.id, "email": user.email, "username": user.username}

        access_token = self.jwt_service.create_access_token(token_data)
        refresh_token = self.jwt_service.create_refresh_token({"sub": user.id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
