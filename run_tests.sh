#!/bin/bash
# Quick test runner for Ebook Generator 1.0
# Run with: ./run_tests.sh

set -e

echo "======================================================================"
echo "  EBOOK GENERATOR 1.0 - TEST SUITE"
echo "======================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Unit Tests
echo -e "${BLUE}🧪 Running Unit Tests from /tests...${NC}"
python3 -m unittest discover tests
echo -e "${GREEN}✅ Unit Tests: PASS${NC}\n"

echo "======================================================================"
echo -e "${GREEN}  ALL TESTS PASSED ✅${NC}"
echo "======================================================================"
echo ""
echo "📊 Summary:"
echo "  • Unit Tests: 10 suites"
echo ""
echo "💡 To run individual tests:"
echo "  python3 -m unittest tests/test_config.py"
echo ""
echo "🚀 To run the main pipeline:"
echo "  uv run src"
echo ""
