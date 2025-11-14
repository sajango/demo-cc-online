#!/bin/bash
# Pre-commit code quality check script
# Run this before committing to ensure your code passes CI checks

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Running code quality checks..."
echo ""

# Track failures
FAILED=0

# Function to print colored status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        FAILED=1
    fi
}

# 1. Check code formatting with Black
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  Checking code formatting with Black..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if black --check --diff src/ tests/ 2>&1; then
    print_status 0 "Black formatting check passed"
else
    print_status 1 "Black formatting check failed"
    echo -e "${YELLOW}💡 Fix with: black src/ tests/${NC}"
fi
echo ""

# 2. Run Flake8 linter
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  Running Flake8 linter..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics; then
    print_status 0 "Flake8 critical errors check passed"
else
    print_status 1 "Flake8 found critical errors"
fi
echo ""

# 3. Run MyPy type checker (warning only)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  Running MyPy type checker..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if mypy src/ --ignore-missing-imports --no-strict-optional 2>&1 | head -20; then
    print_status 0 "MyPy type check completed (warnings allowed)"
else
    echo -e "${YELLOW}⚠️  MyPy found some issues (not blocking)${NC}"
fi
echo ""

# 4. Run unit tests
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣  Running unit tests..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
export DATABASE_URL="mysql+aiomysql://test:test@localhost:3306/test_db"
export REDIS_URL="redis://localhost:6379/0"
export JWT_SECRET_KEY="test-secret-key-for-testing"

if pytest tests/unit/ -v --tb=short; then
    print_status 0 "Unit tests passed"
else
    print_status 1 "Unit tests failed"
fi
echo ""

# 5. Check test coverage (optional)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5️⃣  Checking test coverage..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if pytest tests/unit/ --cov=src --cov-report=term-missing --cov-report=html -q; then
    echo -e "${GREEN}✅ Coverage report generated${NC}"
    echo -e "${YELLOW}💡 View HTML report: open htmlcov/index.html${NC}"
else
    echo -e "${YELLOW}⚠️  Coverage check completed with warnings${NC}"
fi
echo ""

# Final summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! Ready to commit.${NC}"
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Please fix the issues before committing.${NC}"
    exit 1
fi
