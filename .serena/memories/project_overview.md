# Project Overview: demo-cc-online

## Project Identity
- **Name**: demo-cc-online (FastAPI Clean Architecture)
- **Type**: Python FastAPI Web Application
- **Architecture**: Clean Architecture (Domain-Driven Design)
- **Status**: Active Development
- **Primary Language**: Python 3.13
- **Framework**: FastAPI with async/await patterns

## Technology Stack

### Core Framework
- **FastAPI**: Modern async web framework for building APIs
- **Uvicorn**: ASGI server for production deployment
- **Pydantic**: Data validation and settings management

### Database & Persistence
- **MySQL**: Primary database (via aiomysql async driver)
- **SQLAlchemy**: ORM for database operations (async)
- **Alembic**: Database migration management
- **Redis**: Caching layer (async client)

### Dependency Management & DI
- **Injector**: Dependency injection container for IoC
- **Python-dotenv**: Environment variable management

### Authentication & Security
- **JWT (PyJWT)**: Token-based authentication
- **Passlib[bcrypt]**: Password hashing
- **Google OAuth**: Social authentication (Authlib)
- **Apple OAuth**: Social authentication (Authlib)

### Testing & Quality
- **pytest**: Test framework
- **pytest-asyncio**: Async test support
- **pytest-cov**: Code coverage reporting
- **Black**: Code formatting (line-length=100)
- **isort**: Import sorting
- **Flake8**: Linting
- **MyPy**: Type checking (Python 3.11+)

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **MySQL 8.0**: Database container
- **Redis**: Cache container

## Project Purpose
Production-ready FastAPI application template demonstrating:
1. Clean Architecture principles with clear layer separation
2. Domain-Driven Design with rich domain entities
3. Dependency Injection for testability and maintainability
4. Async/await patterns for performance
5. Comprehensive testing strategies
6. Docker-based deployment
7. Database migrations with Alembic
8. JWT and OAuth authentication

## Current State
- ✅ Clean Architecture structure established
- ✅ Domain layer: User entity with repository interface
- ✅ Application layer: User use cases (create, get, register, login, OAuth, refresh)
- ✅ Infrastructure layer: MySQL repository, Redis cache, JWT/password services
- ✅ Presentation layer: FastAPI routes (users, auth)
- ✅ Dependency injection container configured
- ✅ Database migrations: UUID primary keys, authentication fields
- ✅ Unit tests: JWT service, password service, user entity
- ✅ Docker Compose setup for development
- ✅ Documentation: README, CLAUDE.md, PR templates

## Key Design Decisions
1. **Clean Architecture**: Strict layer separation with dependency rule (Domain ← Application ← Infrastructure ← Presentation)
2. **Async First**: All I/O operations use async/await for performance
3. **Type Safety**: Full type hints throughout codebase
4. **UUID Primary Keys**: Using UUID instead of auto-increment integers
5. **Repository Pattern**: Abstract data access through repository interfaces
6. **Use Case Pattern**: Business logic encapsulated in dedicated use case classes
7. **Dependency Injection**: Constructor injection for all dependencies
8. **Environment-based Config**: Pydantic Settings for type-safe configuration
