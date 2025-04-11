"""
This is a test file for the RegexTokenizer.
"""

import pytest
from src import RegexTokenizer
from . import (
    UnclosedGroupError,
)


def test_capture_group_simple():
    """
    Test that a simple capture group (e.g., (abc)) is correctly tokenized.
    """
    sm = RegexTokenizer("(abc)")
    assert sm.tokens == ["(abc)"], "Failed to tokenize a simple capture group."


def test_capture_group_with_escape_sequence():
    """
    Test that a capture group containing an escape sequence (e.g., (a\\n)) is correctly tokenized.
    """
    sm = RegexTokenizer("(a\\n)")
    assert sm.tokens == ["(a\\n)"], "Failed to tokenize a capture group with an escape sequence."


def test_capture_group_unclosed():
    """
    Test that an unclosed capture group (e.g., (abc) raises a UnclosedGroupError.
    """
    with pytest.raises(UnclosedGroupError, match=r"Capture Group was not closed!"):
        RegexTokenizer("(abc")


def test_capture_group_with_nested_parentheses():
    """
    Test that a capture group with nested parentheses (e.g., (a(b)c)) is correctly tokenized.
    """
    sm = RegexTokenizer("(a(b)c)")
    assert sm.tokens == ["(a(b)c)"], "Failed to tokenize a capture group with nested parentheses."


def test_capture_group_with_special_characters():
    """
    Test that a capture group containing special characters (e.g., (a+b*c?)) is correctly tokenized.
    """
    sm = RegexTokenizer("(a+b*c?)")
    assert sm.tokens == ["(a+b*c?)"], "Failed to tokenize a capture group with special characters."


def test_capture_group_with_backslash_at_end():
    """
    Test that a capture group ending with a backslash (e.g., (abc\\)) raises a UnclosedGroupError.
    """
    with pytest.raises(UnclosedGroupError, match=r"Capture Group was not closed!"):
        RegexTokenizer("(abc\\)")
