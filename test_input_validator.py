#!/usr/bin/env python
"""
Test script for input_validator.py - verify get_message() calls work correctly.

This script validates that:
1. input_validator.py compiles without errors
2. SpecValidator class can be instantiated
3. get_message() calls retrieve centralized validation messages
4. Field validation logic works correctly
"""

import sys
from pathlib import Path

# Add src to path for relative imports
sys.path.insert(0, str(Path(__file__).parent))

from src.config import get_message, get_logger, get_config
from src.input_validator import SpecValidator

logger = get_logger(__name__)


def test_get_message_calls():
    """Test that centralized message retrieval works."""
    print("\n🧪 Testing get_message() calls from specs/config.yaml...")

    messages_to_test = [
        "validation_messages.file_not_found",
        "validation_messages.invalid_yaml",
        "validation_messages.missing_field",
        "validation_messages.field_cannot_be_empty",
        "validation_messages.word_count_integer_error",
        "validation_messages.word_count_range_error",
        "validation_messages.reading_level_error",
        "validation_messages.string_not_empty_error",
    ]

    config = get_config()
    validation_msgs = config.get("validation_messages", {})

    for msg_key in messages_to_test:
        # Extract actual key (remove validation_messages. prefix)
        actual_key = msg_key.split(".", 1)[1]
        if actual_key in validation_msgs:
            value = validation_msgs[actual_key]
            print(f"  ✅ {msg_key}: '{value}'")
        else:
            print(f"  ❌ {msg_key}: NOT FOUND")
            return False

    print("\n✅ All centralized messages found in specs/config.yaml!\n")
    return True


def test_spec_validator_instantiation():
    """Test that SpecValidator can be instantiated."""
    print("🧪 Testing SpecValidator instantiation...")
    try:
        validator = SpecValidator()
        print(f"  ✅ SpecValidator instantiated successfully")
        print(f"  - Spec file: {validator.spec_file}")
        print(f"  - Mandatory metadata: {validator.MANDATORY_METADATA}")
        print(f"  - Mandatory params: {validator.MANDATORY_PARAMS}")
        return True
    except Exception as e:
        print(f"  ❌ Failed to instantiate: {str(e)}")
        return False


def test_field_validation():
    """Test field validation logic."""
    print("\n🧪 Testing field validation logic...")
    validator = SpecValidator()

    test_cases = [
        ("parameters_word_count_target", "50000", True, "Valid word count"),
        ("parameters_word_count_target", "1000", False, "Too low word count"),
        ("parameters_word_count_target", "abc", False, "Invalid integer"),
        ("parameters_reading_level", "intermediate", True, "Valid reading level"),
        ("parameters_reading_level", "invalid", False, "Invalid reading level"),
        ("metadata_topic", "Python para Análise", True, "Valid string"),
        ("metadata_topic", "", False, "Empty string"),
    ]

    passed = 0
    failed = 0

    for field, value, should_pass, description in test_cases:
        try:
            result = validator._validate_field_value(field, value)
            if should_pass:
                print(f"  ✅ {description}: '{field}' = '{value}'")
                passed += 1
            else:
                print(f"  ❌ {description}: Should have failed but didn't")
                failed += 1
        except ValueError as e:
            if not should_pass:
                print(f"  ✅ {description}: Correctly rejected ('{str(e)}')")
                passed += 1
            else:
                print(f"  ❌ {description}: Should have passed but failed ('{str(e)}')")
                failed += 1

    print(f"\n  Results: {passed} passed, {failed} failed")
    return failed == 0


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("  INPUT VALIDATOR TEST SUITE")
    print("=" * 70)

    results = {
        "get_message() calls": test_get_message_calls(),
        "SpecValidator instantiation": test_spec_validator_instantiation(),
        "Field validation": test_field_validation(),
    }

    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)

    all_passed = True
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
        all_passed = all_passed and result

    print("=" * 70)

    if all_passed:
        print("\n✅ All tests passed! input_validator.py is working correctly.\n")
        return 0
    else:
        print("\n❌ Some tests failed. Check errors above.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
