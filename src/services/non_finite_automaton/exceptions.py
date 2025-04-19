"""
This module defines custom exceptions for the NFA functionality.
"""


class NFAError(Exception):
    """Base class for all NFA-related errors."""


class InvalidRegexError(NFAError):
    """Raised when the provided regex is invalid."""


class EmptyRegexError(NFAError):
    """Raised when the provided regex is empty."""
