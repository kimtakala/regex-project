"""
This module defines custom exceptions to be used in the shunting yard algorithm.
"""


class StateMachineError(Exception):
    """Base class for all StateMachine-related errors."""


class EscapeSequenceEndError(StateMachineError):
    """Raised when the input ends unexpectedly during an escape sequence."""


class EscapeSequenceLengthError(StateMachineError):
    """Raised when the escape sequence has an incorrect length."""


class EndsWithBackslashError(StateMachineError):
    """Raised when the escape sequence has an incorrect length."""


class UnclosedGroupError(StateMachineError):
    """Raised when a group (e.g., parentheses or brackets) is not closed."""
