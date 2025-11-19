# Architecture: Clean Architecture Layers

## Layer Overview

```
┌─────────────────────────────────────────────┐
│         Presentation Layer (API)            │
│    src/presentation/                        │
│    - FastAPI routes                         │
│    - Pydantic schemas (request/response)    │
└─────────────────────────────────────────────┘
                    ↓ depends on
┌─────────────────────────────────────────────┐
│       Infrastructure Layer                  │
│    src/infrastructure/                      │
│    - Database models (SQLAlchemy)          │
│    - Repository implementations            │
│    - External services (Redis, OAuth)      │
│    - JWT & Password services               │
└─────────────────────────────────────────────┘
                    ↓ depends on
┌─────────────────────────────────────────────┐
│        Application Layer                    │
│    src/application/                         │
│    - Use cases (business logic)             │
│    - Application services                   │
└─────────────────────────────────────────────┘
                    ↓ depends on
┌─────────────────────────────────────────────┐
│          Domain Layer (Core)                │
│    src/domain/                              │
│    - Entities (business objects)            │
│    - Repository interfaces (abstract)      │
│    - Domain exceptions                      │
└─────────────────────────────────────────────┘
```

## Layer Details

### 1. Domain Layer (`src/domain/`)
**Purpose**: Core business entities and abstractions
**Dependencies**: None (innermost layer)

#### Structure:
- `entities/`: Domain entities (User)
  - Rich domain models with business logic
  - Dataclass-based entities
- `repositories/`: Repository interfaces (UserRepository)
  - Abstract base classes defining data access contracts
  - No implementation details

#### Key Files:
- `entities/user.py`: User domain entity
- `repositories/user_repository.py`: User repository interface

### 2. Application Layer (`src/application/`)
**Purpose**: Business logic and use cases
**Dependencies**: Domain layer only

#### Structure:
- `use_cases/`: Business operations
  - `create_user.py`: User creation logic
  - `get_user.py`: User retrieval logic
  - `register_user.py`: User registration with password hashing
  - `login_user.py`: Authentication with JWT generation
  - `refresh_token.py`: Token refresh logic
  - `oauth_login.py`: OAuth authentication flow

#### Pattern:
Each use case class:
- Constructor injection of repository dependencies
- Single `execute()` method for operation
- Returns domain entities or DTOs

### 3. Infrastructure Layer (`src/infrastructure/`)
**Purpose**: External concerns and implementations
**Dependencies**: Domain and Application layers

#### Structure:
- `database/`:
  - `models.py`: SQLAlchemy models (UserModel)
  - `session.py`: Database session management
  - `base.py`: Base model configuration
- `cache/`:
  - `redis_client.py`: Redis async client
- `repositories/`:
  - `user_repository_impl.py`: Concrete UserRepository implementation
- `services/`:
  - `jwt_service.py`: JWT token generation/validation
  - `password_service.py`: Password hashing/verification (Passlib bcrypt)
  - `google_oauth_service.py`: Google OAuth integration
  - `apple_oauth_service.py`: Apple OAuth integration

#### Key Patterns:
- Repository implementations map domain entities ↔ database models
- Services encapsulate external dependencies (JWT, password, OAuth)
- Async operations for all I/O

### 4. Presentation Layer (`src/presentation/`)
**Purpose**: HTTP API and request/response handling
**Dependencies**: All lower layers via dependency injection

#### Structure:
- `api/v1/`:
  - `users.py`: User CRUD endpoints
  - `auth.py`: Authentication endpoints (register, login, refresh, OAuth)
- `schemas/`:
  - `user_schema.py`: User request/response models
  - `auth_schema.py`: Auth request/response models

#### Pattern:
- FastAPI routers with dependency injection
- Pydantic schemas for validation
- HTTP status codes and error handling

### 5. Core Configuration (`src/core/`)
**Purpose**: Application configuration and dependency injection

#### Files:
- `config.py`: Pydantic Settings (database, Redis, JWT config)
- `container.py`: Injector DI container configuration
- `dependencies.py`: FastAPI dependency functions
- `auth_dependencies.py`: JWT authentication dependencies

## Dependency Rule
**Critical**: Dependencies always point inward
- Domain layer: No dependencies
- Application layer: Depends on Domain only
- Infrastructure layer: Depends on Domain + Application
- Presentation layer: Depends on all layers via DI

## Data Flow Example: Create User

```
1. HTTP Request → Presentation Layer
   - POST /api/v1/users/
   - Pydantic schema validates request

2. Presentation → Application Layer
   - Injects CreateUserUseCase
   - Calls use_case.execute()

3. Application → Domain Layer
   - Creates User domain entity
   - Validates business rules

4. Application → Infrastructure
   - Calls UserRepository.create()
   - Repository maps entity → model

5. Infrastructure → Database
   - SQLAlchemy saves UserModel
   - Maps model → entity

6. Return chain
   - Entity → Use Case → Router → HTTP Response
```

## Testing Strategy by Layer

### Domain Layer Tests:
- Pure unit tests
- No external dependencies
- Test business logic and validation

### Application Layer Tests:
- Mock repository dependencies
- Test use case orchestration
- Test business workflows

### Infrastructure Layer Tests:
- Integration tests with real database/Redis
- Test repository implementations
- Test service integrations

### Presentation Layer Tests:
- API endpoint tests
- Test HTTP contracts
- End-to-end request/response validation
