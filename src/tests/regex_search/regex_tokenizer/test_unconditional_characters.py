"""
This is a test file for the unconditional characters in RegexTokenizer.
"""

import re
import pytest
from src import RegexTokenizer
from . import (
    EndsWithBackslashError,
)


def test_unconditional_characters():
    """
    Test that unconditional characters (letters, digits, and '.') are correctly tokenized.
    """
    sm = RegexTokenizer("abc123.")
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
    with pytest.raises(
        EndsWithBackslashError, match=re.escape('input string cannot end in a backslash "\\"')
    ):
        RegexTokenizer("abc\\")
