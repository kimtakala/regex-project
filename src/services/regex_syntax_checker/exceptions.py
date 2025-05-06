"""
This module defines custom exceptions to be used in the shunting yard algorithm.
"""


class RegexTokenizerError(Exception):
    """Base class for all StateMachine-related errors."""


class EscapeSequenceEndError(RegexTokenizerError):
    """Raised when the input ends unexpectedly during an escape sequence."""


class EscapeSequenceLengthError(RegexTokenizerError):
    """Raised when the escape sequence has an incorrect length."""


class EndsWithBackslashError(RegexTokenizerError):
    """Raised when the escape sequence has an incorrect length."""


class UnclosedGroupError(RegexTokenizerError):
    """Raised when a group (e.g., parentheses or brackets) is not closed."""
