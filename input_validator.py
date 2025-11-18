"""Compatibility wrapper to expose the SpecValidator at the project root."""

from src.input_validator import SpecValidator, validate_book_input

__all__ = ["SpecValidator", "validate_book_input"]
