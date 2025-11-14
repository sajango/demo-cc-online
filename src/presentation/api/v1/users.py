from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_db
from src.presentation.schemas.user_schema import UserCreate, UserResponse
from src.application.use_cases.create_user import CreateUserUseCase
from src.application.use_cases.get_user import GetUserUseCase
from src.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new user"""
    repository = UserRepositoryImpl(db)
    use_case = CreateUserUseCase(repository)

    try:
        user = await use_case.execute(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get user by ID"""
    repository = UserRepositoryImpl(db)
    use_case = GetUserUseCase(repository)

    user = await use_case.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all users with pagination"""
    repository = UserRepositoryImpl(db)
    use_case = GetUserUseCase(repository)

    users = await use_case.get_all(skip=skip, limit=limit)
    return users
