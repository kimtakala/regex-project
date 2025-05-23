"""
Tests for square brackets in RegexTokenizer
"""

import pytest
import re
from src import RegexTokenizer
from . import (
    RegexTokenizerError,
    UnclosedGroupError,
)


def test_square_brackets_simple():
    """
    Test that simple character sets (e.g., [abc]) are correctly tokenized.
    """
    sm = RegexTokenizer("[abc]")
    assert sm.tokens == ["[abc]"], "Failed to tokenize a simple character set."


def test_square_brackets_with_caret():
    """
    Test that negated character sets (e.g., [^abc]) are correctly tokenized.
    """
    sm = RegexTokenizer("[^abc]")
    assert sm.tokens == ["[^abc]"], "Failed to tokenize a negated character set."


def test_square_brackets_with_dash():
    """
    Test that character ranges (e.g., [a-z]) are correctly tokenized.
    """
    sm = RegexTokenizer("[a-z]")
    assert sm.tokens == ["[a-z]"], "Failed to tokenize a character range."


def test_square_brackets_unclosed():
    """
    Test that unclosed square brackets raise a UnclosedGroupError.
    """
    with pytest.raises(UnclosedGroupError, match=r"Squarebracket character set was not closed!"):
        RegexTokenizer("[abc")


def test_invalid_range_in_square_brackets():
    """
    Test that invalid ranges in square brackets (e.g., [a-b-c]) raise a RegexTokenizerError.
    """
    with pytest.raises(
        RegexTokenizerError,
        match=r"Invalid range: 'b-c' uses a range character with an already used range.",
    ):
        RegexTokenizer("[a-b-c]")


def test_square_brackets_with_escape_sequence():
    """
    Test that square brackets containing escape sequences (e.g., [a\\z]) are correctly tokenized.
    """
    sm = RegexTokenizer("[a\\z]")
    assert sm.tokens == ["[a\\z]"], "Failed to tokenize square brackets with an escaped backslash."


def test_square_brackets_with_literal_dash():
    """
    Test that square brackets containing a literal dash (e.g., [-abc]) are correctly tokenized.
    """
    sm = RegexTokenizer("[-abc]")
    assert sm.tokens == ["[-abc]"], "Failed to tokenize square brackets with a literal dash."


def test_square_brackets_with_literal_dash_at_end():
    """
    Test that square brackets containing a literal dash at the end (e.g., [abc-]) are correctly tokenized.
    """
    sm = RegexTokenizer("[abc-]")
    assert sm.tokens == [
        "[abc-]"
    ], "Failed to tokenize square brackets with a literal dash at the end."


def test_square_brackets_with_literal_dash_at_start():
    """
    Test that square brackets containing a literal dash at the start (e.g., [-a]) are correctly tokenized.
    """
    sm = RegexTokenizer("[-a]")
    assert sm.tokens == [
        "[-a]"
    ], "Failed to tokenize square brackets with a literal dash at the start."


def test_square_brackets_caret_only():
    """
    Test that a character set with only '^' (e.g., [^]) raises a RegexTokenizerError.
    """
    with pytest.raises(
        RegexTokenizerError,
        match=re.escape('"^" cannot be the only character in a character set!'),
    ):
        RegexTokenizer("[^]")


def test_square_brackets_with_only_literal_dash():
    """
    Test that square brackets containing only a literal dash (e.g., [-]) are correctly tokenized.
    """
    sm = RegexTokenizer("[-]")
    assert sm.tokens == ["[-]"], "Failed to tokenize square brackets with only a literal dash."
