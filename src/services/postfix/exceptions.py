"""
This module defines custom exceptions for the postfix functionality.
"""


class PostfixError(Exception):
    """Base class for all postfix-related errors."""


class MismatchedParenthesesError(PostfixError):
    """Raised when there are mismatched parentheses in the input."""
