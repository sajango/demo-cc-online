from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_db
from src.core.auth_dependencies import get_current_user
from src.presentation.schemas.auth_schema import (
    UserRegister,
    UserLogin,
    TokenResponse,
    RefreshTokenRequest,
    GoogleAuthRequest,
    AppleAuthRequest
)
from src.presentation.schemas.user_schema import UserResponse
from src.application.use_cases.register_user import RegisterUserUseCase
from src.application.use_cases.login_user import LoginUserUseCase
from src.application.use_cases.refresh_token import RefreshTokenUseCase
from src.application.use_cases.oauth_login import OAuthLoginUseCase
from src.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.infrastructure.services.password_service import PasswordService
from src.infrastructure.services.jwt_service import JWTService
from src.infrastructure.services.google_oauth_service import GoogleOAuthService
from src.infrastructure.services.apple_oauth_service import AppleOAuthService

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user with email and password"""
    repository = UserRepositoryImpl(db)
    password_service = PasswordService()
    use_case = RegisterUserUseCase(repository, password_service)

    try:
        user = await use_case.execute(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            password=user_data.password
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login with email and password"""
    repository = UserRepositoryImpl(db)
    password_service = PasswordService()
    jwt_service = JWTService()
    use_case = LoginUserUseCase(repository, password_service, jwt_service)

    try:
        tokens = await use_case.execute(
            email=credentials.email,
            password=credentials.password
        )
        return tokens
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token using refresh token"""
    repository = UserRepositoryImpl(db)
    jwt_service = JWTService()
    use_case = RefreshTokenUseCase(repository, jwt_service)

    try:
        tokens = await use_case.execute(request.refresh_token)
        return tokens
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/google", response_model=TokenResponse)
async def google_auth(
    request: GoogleAuthRequest,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate with Google OAuth"""
    google_service = GoogleOAuthService()

    # Verify Google ID token
    user_info = await google_service.verify_id_token(request.id_token)

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google ID token"
        )

    # Login or register user
    repository = UserRepositoryImpl(db)
    jwt_service = JWTService()
    use_case = OAuthLoginUseCase(repository, jwt_service)

    try:
        tokens = await use_case.execute(
            email=user_info["email"],
            full_name=user_info["full_name"],
            provider="google",
            provider_user_id=user_info["provider_user_id"]
        )
        return tokens
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/apple", response_model=TokenResponse)
async def apple_auth(
    request: AppleAuthRequest,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate with Apple Sign-In"""
    apple_service = AppleOAuthService()

    # Verify Apple ID token
    user_info = await apple_service.verify_id_token(request.id_token)

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Apple ID token"
        )

    # Login or register user
    repository = UserRepositoryImpl(db)
    jwt_service = JWTService()
    use_case = OAuthLoginUseCase(repository, jwt_service)

    try:
        tokens = await use_case.execute(
            email=user_info["email"],
            full_name=user_info["full_name"] or user_info["email"].split("@")[0],
            provider="apple",
            provider_user_id=user_info["provider_user_id"]
        )
        return tokens
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user = Depends(get_current_user)
):
    """Get current authenticated user information"""
    return current_user
