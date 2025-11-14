# FastAPI Clean Architecture Project

A production-ready FastAPI project template implementing Clean Architecture principles with Docker, MySQL, Redis, and dependency injection.

## Features

- **Clean Architecture**: Separation of concerns with Domain, Application, Infrastructure, and Presentation layers
- **FastAPI**: Modern, fast web framework for building APIs
- **Docker**: Containerized application with Docker Compose
- **MySQL**: Async database operations with SQLAlchemy
- **Redis**: Caching support with async Redis client
- **Dependency Injection**: Using Injector for IoC container
- **Database Migrations**: Alembic for schema management
- **Type Safety**: Full type hints throughout the codebase
- **Testing Ready**: Structured test directory with pytest

## Project Structure

```
demo-cc-online/
├── src/
│   ├── domain/                 # Domain layer (Business entities)
│   │   ├── entities/          # Domain entities
│   │   └── repositories/      # Repository interfaces
│   ├── application/           # Application layer (Use cases)
│   │   └── use_cases/        # Business logic use cases
│   ├── infrastructure/        # Infrastructure layer (External services)
│   │   ├── database/         # Database configuration and models
│   │   ├── cache/            # Redis cache client
│   │   └── repositories/     # Repository implementations
│   ├── presentation/          # Presentation layer (API)
│   │   ├── api/              # API routes
│   │   └── schemas/          # Pydantic schemas
│   ├── core/                  # Core configurations
│   │   ├── config.py         # Application settings
│   │   ├── container.py      # Dependency injection container
│   │   └── dependencies.py   # FastAPI dependencies
│   └── main.py               # Application entry point
├── tests/                     # Test files
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
├── alembic/                   # Database migrations
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                # Docker image definition
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Clean Architecture Layers

### 1. Domain Layer
The innermost layer containing business entities and repository interfaces.
- **Entities**: Core business objects (e.g., User)
- **Repository Interfaces**: Abstract definitions for data access

### 2. Application Layer
Contains business logic and use cases.
- **Use Cases**: Specific business operations (e.g., CreateUserUseCase)

### 3. Infrastructure Layer
Implements external concerns and dependencies.
- **Database Models**: SQLAlchemy models
- **Repository Implementations**: Concrete repository classes
- **External Services**: Redis, third-party APIs, etc.

### 4. Presentation Layer
Handles HTTP requests and responses.
- **API Routes**: FastAPI endpoints
- **Schemas**: Request/response validation with Pydantic

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

## Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd demo-cc-online
```

### 2. Create environment file

```bash
cp .env.example .env
```

Edit `.env` file with your configuration if needed.

### 3. Start with Docker Compose

```bash
docker-compose up -d
```

This will start:
- FastAPI application on `http://localhost:8000`
- MySQL database on `localhost:3306`
- Redis cache on `localhost:6379`

### 4. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Local Development

### Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/app_db
REDIS_URL=redis://localhost:6379/0
ENVIRONMENT=development
DEBUG=True
```

### Database Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback migration:

```bash
alembic downgrade -1
```

### Run the Application

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Users

- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `GET /api/v1/users/` - List all users (with pagination)

### Example Request

Create a user:

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe"
  }'
```

## Testing

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=src tests/
```

## Docker Commands

Build and start containers:

```bash
docker-compose up --build
```

Stop containers:

```bash
docker-compose down
```

View logs:

```bash
docker-compose logs -f app
```

Access database:

```bash
docker-compose exec mysql mysql -u user -ppassword app_db
```

Access Redis CLI:

```bash
docker-compose exec redis redis-cli
```

## Adding New Features

### 1. Create Domain Entity

```python
# src/domain/entities/product.py
from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    price: float
```

### 2. Define Repository Interface

```python
# src/domain/repositories/product_repository.py
from abc import ABC, abstractmethod

class ProductRepository(ABC):
    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass
```

### 3. Implement Repository

```python
# src/infrastructure/repositories/product_repository_impl.py
class ProductRepositoryImpl(ProductRepository):
    async def create(self, product: Product) -> Product:
        # Implementation
        pass
```

### 4. Create Use Case

```python
# src/application/use_cases/create_product.py
class CreateProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def execute(self, name: str, price: float) -> Product:
        # Business logic
        pass
```

### 5. Add API Endpoint

```python
# src/presentation/api/v1/products.py
@router.post("/")
async def create_product(data: ProductCreate):
    # Handle request
    pass
```

## Dependencies

Key dependencies:

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **sqlalchemy**: ORM for database
- **aiomysql**: Async MySQL driver
- **redis**: Redis client
- **injector**: Dependency injection
- **pydantic**: Data validation
- **alembic**: Database migrations

See `requirements.txt` for full list.

## Best Practices

1. **Separation of Concerns**: Keep layers independent
2. **Dependency Rule**: Dependencies point inward (Domain ← Application ← Infrastructure)
3. **Type Hints**: Use type annotations throughout
4. **Async/Await**: Use async operations for I/O
5. **Error Handling**: Use domain exceptions and map to HTTP errors
6. **Testing**: Write tests for each layer independently

## Configuration

Application settings in `src/core/config.py`:

- Environment-based configuration
- Type-safe settings with Pydantic
- Override via environment variables

## Troubleshooting

### Database Connection Issues

Check MySQL is running:
```bash
docker-compose ps
```

View MySQL logs:
```bash
docker-compose logs mysql
```

### Redis Connection Issues

Test Redis connection:
```bash
docker-compose exec redis redis-cli ping
```

### Application Errors

View application logs:
```bash
docker-compose logs -f app
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Update documentation
5. Submit a pull request

## License

[Your License Here]

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
