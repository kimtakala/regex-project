class StateMachineError(Exception):
    """Base class for all StateMachine-related errors."""

    pass


class EscapeSequenceEndError(StateMachineError):
    """Raised when the input ends unexpectedly during an escape sequence."""

    pass


class EscapeSequenceLengthError(StateMachineError):
    """Raised when the escape sequence has an incorrect length."""

    pass


class EndsWithBackslashError(StateMachineError):
    """Raised when the escape sequence has an incorrect length."""

    pass


class UnclosedGroupError(StateMachineError):
    """Raised when a group (e.g., parentheses or brackets) is not closed."""

    pass
