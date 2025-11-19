# Development Workflows & Commands

## Environment Setup

### Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables
```bash
# Copy template
cp .env.example .env

# Edit configuration
# DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/app_db
# REDIS_URL=redis://localhost:6379/0
# JWT_SECRET_KEY=your-secret-key-here
```

## Docker Workflows

### Development with Docker Compose
```bash
# Start all services (app, MySQL, Redis)
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Rebuild after dependency changes
docker-compose up --build
```

### Individual Container Commands
```bash
# MySQL access
docker-compose exec mysql mysql -u user -ppassword app_db

# Redis CLI
docker-compose exec redis redis-cli

# Application shell
docker-compose exec app bash
```

## Database Management

### Alembic Migrations

#### Create Migration
```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "description of changes"

# Example: alembic revision --autogenerate -m "add user authentication fields"
```

#### Apply Migrations
```bash
# Upgrade to latest
alembic upgrade head

# Upgrade one version
alembic upgrade +1

# Downgrade one version
alembic downgrade -1

# Check current version
alembic current

# View migration history
alembic history
```

#### Migration File Pattern
```python
# alembic/versions/xxx_description.py
def upgrade():
    op.add_column('users', sa.Column('new_field', sa.String(50)))

def downgrade():
    op.drop_column('users', 'new_field')
```

## Code Quality & Testing

### Formatting
```bash
# Black formatting (line-length=100)
black src/ tests/

# Check without changes
black --check src/ tests/

# Format specific file
black src/domain/entities/user.py
```

### Import Sorting
```bash
# Sort imports with isort
isort src/ tests/

# Check without changes
isort --check-only src/ tests/
```

### Linting
```bash
# Flake8 linting
flake8 src/ tests/

# With configuration from .flake8
# Max line length: 100
# Ignore: E203, W503 (Black compatibility)
```

### Type Checking
```bash
# MyPy type checking
mypy src/

# Check specific module
mypy src/domain/
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/unit/test_user_entity.py

# Run specific test
pytest tests/unit/test_user_entity.py::test_user_creation

# Run with verbose output
pytest -v

# Run unit tests only
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run with markers
pytest -m unit
pytest -m integration
```

### Combined Quality Check
```bash
# Format, lint, type-check, test (all at once)
black src/ tests/ && \
isort src/ tests/ && \
flake8 src/ tests/ && \
mypy src/ && \
pytest --cov=src tests/
```

## Running the Application

### Local Development
```bash
# Run with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run with specific log level
uvicorn src.main:app --reload --log-level debug

# Run without reload (production-like)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Access
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Git Workflow

### Branch Strategy
```bash
# Current feature branch (AI assistant)
git checkout claude/claude-md-{session-id}

# Create new feature branch
git checkout -b feature/authentication

# View current branch
git branch
```

### Commit Process
```bash
# Stage changes
git add .

# Commit with conventional format
git commit -m "feat: add user authentication"
git commit -m "fix(api): resolve race condition in user creation"
git commit -m "docs: update README with setup instructions"

# Push to remote
git push -u origin claude/claude-md-{session-id}
```

### Commit Types
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting
- `refactor:` - Code restructuring
- `test:` - Tests
- `chore:` - Maintenance
- `perf:` - Performance

## Dependency Management

### Adding Dependencies
```bash
# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

### Dependency Categories in requirements.txt
```
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
aiomysql==0.2.0
alembic==1.12.1

# Authentication
PyJWT==2.8.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
```

## Debugging

### FastAPI Debugging
```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use built-in breakpoint()
breakpoint()
```

### Logging
```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Docker Debugging
```bash
# View container logs
docker-compose logs -f app

# Access container shell
docker-compose exec app bash

# Inspect container
docker inspect demo-cc-online-app
```

## Performance Profiling

### Database Query Logging
```python
# Enable in src/infrastructure/database/session.py
engine = create_async_engine(
    DATABASE_URL,
    echo=True  # SQL logging
)
```

### API Performance
```bash
# Use httpie for testing
http POST http://localhost:8000/api/v1/users/ \
  email=test@example.com \
  username=testuser

# Use curl
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser"}'
```

## Common Issues & Solutions

### Port Already in Use
```bash
# Find process on port 8000
lsof -ti:8000

# Kill process
kill -9 <PID>
```

### Database Connection Refused
```bash
# Check MySQL is running
docker-compose ps mysql

# Restart MySQL
docker-compose restart mysql

# View MySQL logs
docker-compose logs mysql
```

### Migration Conflicts
```bash
# Check current migration
alembic current

# Stamp database to specific revision
alembic stamp head

# Resolve conflicts manually in versions/
```

### Redis Connection Issues
```bash
# Check Redis is running
docker-compose ps redis

# Test connection
docker-compose exec redis redis-cli ping

# Flush Redis cache
docker-compose exec redis redis-cli FLUSHALL
```
