"""
This is a test file for the StateMachine.
"""

import pytest
from src import StateMachine
from . import (
    StateMachineError,
)


def test_escape_sequence():
    """
    Test that escape sequences (e.g., \n) are correctly tokenized.
    """
    sm = StateMachine("\\n")
    assert sm.tokens == ["\\n"], "Failed to correctly tokenize an escape sequence."


def test_incomplete_escape_sequence():
    """
    Test that incomplete escape sequences raise a StateMachineError.
    """
    with pytest.raises(
        StateMachineError,
        match=r'Invalid escape sequence "\\\\x1" at index 0. Expected hexadecimal characters.',
    ):
        StateMachine("\\x1")
