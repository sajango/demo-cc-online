# GitHub Actions Workflows

This directory contains CI/CD workflows for automated code quality checks and testing.

## Workflows

### 1. CI - Code Quality & Tests (`ci.yml`)

**Triggers:**
- Push to `main`, `master`, `develop`, or any `claude/**` branch
- Pull requests to `main`, `master`, or `develop`

**Jobs:**

#### Code Quality Checks
- **Black**: Code formatting validation
- **Flake8**: Code linting and style checks
- **MyPy**: Static type checking (continues on error)

#### Tests
- Runs on Python 3.11 and 3.12
- Executes unit tests with pytest
- Generates code coverage reports (80% threshold recommended)
- Uploads coverage artifacts

#### Integration Tests
- Runs with MySQL and Redis Docker services
- Executes database migrations
- Runs integration tests (if available)

#### Security Scan
- **Safety**: Checks dependencies for known vulnerabilities
- **Bandit**: Scans code for security issues
- Uploads security reports as artifacts

#### Build Status Summary
- Provides final status of all checks
- Fails the build if code quality or tests fail

---

### 2. PR Quick Check (`pr-quick-check.yml`)

**Triggers:**
- Pull request opened, synchronized, or reopened

**Purpose:**
Fast feedback for pull requests before full CI runs.

**Checks:**
- Code formatting on changed files only (Black)
- Syntax validation on changed files (Flake8)
- Quick unit test run

---

## Configuration Files

### `.flake8`
Configuration for Flake8 linter:
- Max line length: 100
- Max complexity: 10
- Ignores conflicts with Black

### `pyproject.toml`
Configuration for:
- **Black**: Code formatter settings
- **Pytest**: Test discovery and options
- **Coverage**: Coverage reporting configuration
- **MyPy**: Type checking settings
- **isort**: Import sorting (compatible with Black)

### `pytest.ini`
Additional pytest configuration:
- Test discovery patterns
- Output formatting
- Test markers (unit, integration, slow, auth, database, oauth)

---

## Running Locally

### Code Quality Checks

```bash
# Format code with Black
black src/ tests/

# Check formatting without changes
black --check src/ tests/

# Run Flake8 linter
flake8 src/ tests/

# Run MyPy type checker
mypy src/ --ignore-missing-imports
```

### Testing

```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific marker
pytest -m unit
pytest -m auth
```

### Security Checks

```bash
# Install tools
pip install safety bandit

# Check dependencies
safety check

# Scan code for security issues
bandit -r src/
```

---

## Coverage Reports

Coverage reports are generated for Python 3.11 runs and uploaded as artifacts:
- HTML report in `htmlcov/`
- XML report in `coverage.xml`

Download from Actions → Artifacts section.

---

## Status Badges

Add to your README.md:

```markdown
![CI](https://github.com/YOUR_USERNAME/demo-cc-online/workflows/CI%20-%20Code%20Quality%20%26%20Tests/badge.svg)
```

---

## Troubleshooting

### Tests Failing Locally but Passing in CI
- Check environment variables (DATABASE_URL, REDIS_URL, JWT_SECRET_KEY)
- Ensure dependencies are up to date: `pip install -r requirements.txt`
- Clear pytest cache: `rm -rf .pytest_cache`

### Flake8 and Black Conflicts
- Configuration ensures compatibility
- Run `black` first, then `flake8`

### Coverage Threshold Failures
- Current threshold: 60%
- Increase by adding more unit tests
- Adjust threshold in `ci.yml` if needed

---

## Best Practices

1. **Before committing:**
   - Run `black src/ tests/`
   - Run `pytest tests/unit/`
   - Fix any Flake8 errors

2. **For pull requests:**
   - Ensure all tests pass
   - Add tests for new features
   - Update documentation if needed

3. **Security:**
   - Never commit secrets or credentials
   - Review Bandit findings
   - Keep dependencies updated

---

## Customization

### Modify Python Versions
Edit `ci.yml` matrix:
```yaml
strategy:
  matrix:
    python-version: ['3.11', '3.12']  # Add more versions
```

### Adjust Coverage Threshold
Edit `ci.yml`:
```yaml
coverage report --fail-under=60  # Change threshold
```

### Add Custom Checks
Add new jobs to `ci.yml` following existing patterns.

---

## Support

For issues with workflows:
1. Check workflow logs in Actions tab
2. Review configuration files
3. Consult [GitHub Actions documentation](https://docs.github.com/en/actions)
