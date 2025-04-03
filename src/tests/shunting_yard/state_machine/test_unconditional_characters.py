"""
This is a test file for the StateMachine.
"""

import pytest
import re
from src import StateMachine
from . import (
    StateMachineError,
    EndsWithBackslashError,
    EscapeSequenceEndError,
    EscapeSequenceLengthError,
    UnclosedGroupError,
)


def test_unconditional_characters():
    """
    Test that unconditional characters (letters, digits, and '.') are correctly tokenized.
    """
    sm = StateMachine("abc123.")
    sm.tokenize()
    assert sm.tokens == [
        "a",
        "b",
        "c",
        "1",
        "2",
        "3",
        ".",
    ], "Failed to tokenize unconditional characters."


def test_backslash_at_end():
    """
    Test that a backslash at the end of the input string raises a EndsWithBackslashError.
    """
    sm = StateMachine("abc\\")
    with pytest.raises(
        EndsWithBackslashError, match=re.escape('input string cannot end in a backslash "\\"')
    ):
        sm.tokenize()
