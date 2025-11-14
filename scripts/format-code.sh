#!/bin/bash
# Auto-format code with Black

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🎨 Formatting code with Black..."
echo ""

# Format Python code
black src/ tests/

echo ""
echo -e "${GREEN}✅ Code formatting complete!${NC}"
echo ""
echo -e "${YELLOW}💡 Tip: Run 'scripts/check-code.sh' to verify all checks before committing${NC}"
