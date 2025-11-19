# Codebase Conventions & Patterns

## Python Code Style

### Formatting
- **Line Length**: 100 characters (Black configuration)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes for strings (Black default)
- **Import Sorting**: isort with Black profile
- **Type Hints**: Full type annotations throughout

### Naming Conventions
- **Variables**: `snake_case`
- **Functions**: `snake_case` (verb-based)
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore` for internal methods/properties
- **Files**: `snake_case.py`
- **Packages**: `lowercase` (single word when possible)

### Examples:
```python
# Variables
user_id: str
active_users: list[User]

# Functions
def create_user(email: str) -> User:
    pass

# Classes
class UserRepository:
    pass

# Constants
MAX_LOGIN_ATTEMPTS = 5
DEFAULT_PAGE_SIZE = 20

# Private
def _validate_email(email: str) -> bool:
    pass
```

## Async/Await Patterns

### Rules:
1. **All I/O operations MUST be async**:
   - Database queries
   - Redis operations
   - External API calls
   - File I/O

2. **Repository methods MUST be async**:
   ```python
   async def create(self, entity: User) -> User:
       pass
   ```

3. **Use case execute() MUST be async**:
   ```python
   async def execute(self, data: dict) -> User:
       pass
   ```

4. **FastAPI routes MUST be async**:
   ```python
   @router.post("/")
   async def create_user(data: UserCreate):
       pass
   ```

### Best Practices:
- Use `async with` for async context managers
- Prefer `asyncio.gather()` for parallel operations
- Use `async for` for async iterators
- Avoid blocking operations in async code

## Dependency Injection Patterns

### Constructor Injection (Preferred):
```python
class CreateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def execute(self, data: dict) -> User:
        return await self.repository.create(User(**data))
```

### Container Configuration:
```python
# src/core/container.py
def configure(binder):
    binder.bind(UserRepository, to=UserRepositoryImpl, scope=singleton)
```

### FastAPI Dependency:
```python
# src/core/dependencies.py
def get_user_repository() -> UserRepository:
    return container.get(UserRepository)

# Usage in router
@router.post("/")
async def create_user(
    data: UserCreate,
    repo: UserRepository = Depends(get_user_repository)
):
    pass
```

## Repository Pattern

### Interface (Domain Layer):
```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: str) -> User | None:
        pass
```

### Implementation (Infrastructure Layer):
```python
class UserRepositoryImpl(UserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user: User) -> User:
        model = self._to_model(user)
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return self._to_entity(model)
    
    def _to_model(self, entity: User) -> UserModel:
        """Map domain entity to database model"""
        pass
    
    def _to_entity(self, model: UserModel) -> User:
        """Map database model to domain entity"""
        pass
```

## Use Case Pattern

### Structure:
```python
class UseCase:
    def __init__(self, repository: Repository):
        """Constructor injection of dependencies"""
        self.repository = repository
    
    async def execute(self, input_data: dict) -> OutputEntity:
        """
        Single public method for use case execution
        Returns domain entities or DTOs
        """
        pass
```

### Example:
```python
class LoginUserUseCase:
    def __init__(
        self,
        repository: UserRepository,
        password_service: PasswordService,
        jwt_service: JWTService
    ):
        self.repository = repository
        self.password_service = password_service
        self.jwt_service = jwt_service
    
    async def execute(self, email: str, password: str) -> dict:
        user = await self.repository.find_by_email(email)
        if not user or not self.password_service.verify(password, user.password_hash):
            raise InvalidCredentialsError()
        
        access_token = self.jwt_service.create_access_token(user.id)
        refresh_token = self.jwt_service.create_refresh_token(user.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
```

## Pydantic Schema Pattern

### Request/Response Separation:
```python
# Request schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    full_name: str | None = None

# Response schemas
class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: str | None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
```

### Validation:
```python
from pydantic import field_validator, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v
```

## Error Handling

### Domain Exceptions:
```python
# src/domain/exceptions.py
class DomainException(Exception):
    """Base domain exception"""
    pass

class UserNotFoundError(DomainException):
    pass

class InvalidCredentialsError(DomainException):
    pass
```

### HTTP Exception Mapping:
```python
from fastapi import HTTPException, status

try:
    user = await use_case.execute(data)
except UserNotFoundError:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
except InvalidCredentialsError:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )
```

## Database Patterns

### SQLAlchemy Model:
```python
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.mysql import CHAR
import uuid
from datetime import datetime

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Session Management:
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
```

## Testing Patterns

### Unit Test Structure (AAA Pattern):
```python
import pytest

@pytest.mark.asyncio
async def test_create_user_success():
    # Arrange
    repository = MockUserRepository()
    use_case = CreateUserUseCase(repository)
    data = {"email": "test@example.com", "username": "testuser"}
    
    # Act
    result = await use_case.execute(data)
    
    # Assert
    assert result.email == "test@example.com"
    assert result.username == "testuser"
```

### Fixtures:
```python
@pytest.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture
def user_repository(db_session):
    return UserRepositoryImpl(db_session)
```

## Configuration Management

### Settings (Pydantic):
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )
```

### Environment Variables:
- `.env` for local development
- `.env.example` for template
- Docker Compose for container environment
- Never commit `.env` files

## Import Organization (isort)

```python
# 1. Standard library
import asyncio
from datetime import datetime
from typing import Optional

# 2. Third-party
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

# 3. First-party (src)
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.application.use_cases.create_user import CreateUserUseCase
```
