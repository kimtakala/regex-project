"""
This is a test file for the RegexTokenizer.
"""

import pytest
from src import RegexTokenizer
from . import (
    RegexTokenizerError,
    EscapeSequenceLengthError,
    EscapeSequenceEndError,
)


def test_escape_sequence():
    """
    Test that escape sequences (e.g., \n) are correctly tokenized.
    """
    sm = RegexTokenizer("\\n")
    assert sm.tokens == ["\\n"], "Failed to correctly tokenize an escape sequence."


def test_incomplete_escape_sequence():
    """
    Test that incomplete escape sequences raise a RegexTokenizerError.
    """
    with pytest.raises(
        RegexTokenizerError,
        match=r"Incomplete escape sequence",
    ):
        RegexTokenizer("\\u1")


def test_incomplete_escape_sequence_length_error():
    """
    Test that incomplete escape sequences raise an EscapeSequenceLengthError.
    """
    with pytest.raises(
        EscapeSequenceLengthError,
        match=r"Incomplete escape sequence",
    ):
        RegexTokenizer("\\x0")
