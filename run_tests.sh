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

# Test 1: Input Validator
echo -e "${BLUE}🧪 Running Input Validator Tests...${NC}"
uv run test_input_validator.py
echo -e "${GREEN}✅ Input Validator: PASS${NC}\n"

# Test 2: TUI Output
echo -e "${BLUE}🧪 Running Rich TUI Output Tests...${NC}"
uv run test_tui_output.py
echo -e "${GREEN}✅ TUI Output: PASS${NC}\n"

# Test 3: End-to-End Pipeline
echo -e "${BLUE}🧪 Running End-to-End Pipeline Tests...${NC}"
uv run test_e2e_pipeline.py
echo -e "${GREEN}✅ End-to-End Pipeline: PASS${NC}\n"

echo "======================================================================"
echo -e "${GREEN}  ALL TESTS PASSED ✅${NC}"
echo "======================================================================"
echo ""
echo "📊 Summary:"
echo "  • test_input_validator.py: 3 suites, 7 assertions"
echo "  • test_tui_output.py: 5 suites, 15+ assertions"
echo "  • test_e2e_pipeline.py: 5 suites, 20+ assertions"
echo ""
echo "💡 To run individual tests:"
echo "  uv run test_input_validator.py"
echo "  uv run test_tui_output.py"
echo "  uv run test_e2e_pipeline.py"
echo ""
echo "🚀 To run the main pipeline:"
echo "  uv run src"
echo ""
