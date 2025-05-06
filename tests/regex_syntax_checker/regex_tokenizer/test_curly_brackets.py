"""
Tests for curly braces in RegexTokenizer
"""

import pytest
from src import RegexTokenizer
from . import (
    RegexTokenizerError,
    UnclosedGroupError,
)


def test_curly_brackets_exact_number():
    """
    Test that a quantifier with an exact number (e.g., {5}) is correctly tokenized.
    """
    sm = RegexTokenizer("a{5}")
    assert sm.tokens == ["a", "{5}"], "Failed to tokenize a quantifier with an exact number."


def test_curly_brackets_minimum_number():
    """
    Test that a quantifier with a minimum number (e.g., {2,}) is correctly tokenized.
    """
    sm = RegexTokenizer("a{2,}")
    assert sm.tokens == ["a", "{2,}"], "Failed to tokenize a quantifier with a minimum number."


def test_curly_brackets_range():
    """
    Test that a quantifier with a range (e.g., {1,3}) is correctly tokenized.
    """
    sm = RegexTokenizer("a{1,3}")
    assert sm.tokens == ["a", "{1,3}"], "Failed to tokenize a quantifier with a range."


def test_curly_brackets_unclosed():
    """
    Test that an unclosed quantifier (e.g., {5) raises a UnclosedGroupError.
    """
    with pytest.raises(UnclosedGroupError, match=r"Quantifier braces were not closed!"):
        RegexTokenizer("a{5")


def test_curly_brackets_multiple_commas():
    """
    Test that a quantifier with multiple commas (e.g., {1,3,}) raises a RegexTokenizerError.
    """
    with pytest.raises(
        RegexTokenizerError, match=r"Quantifier braces cannot include multiple commas!"
    ):
        RegexTokenizer("a{1,3,}")


def test_curly_brackets_start_with_comma():
    """
    Test that a quantifier starting with a comma (e.g., {,5}) raises a RegexTokenizerError.
    """
    with pytest.raises(
        RegexTokenizerError,
        match=r"Quantifier braces cannot start with a comma! Ensure the format is {n} or {n,m}.",
    ):
        RegexTokenizer("a{,5}")


def test_curly_brackets_non_rising_range():
    """
    Test that a quantifier with a non-rising range (e.g., {3,1}) raises a RegexTokenizerError.
    """
    with pytest.raises(
        RegexTokenizerError, match=r"Range specified in quantifier braces must be rising!"
    ):
        RegexTokenizer("a{3,1}")


def test_curly_brackets_invalid_character():
    """
    Test that a quantifier with invalid characters (e.g., {1,a}) raises a RegexTokenizerError.
    """
    with pytest.raises(
        RegexTokenizerError,
        match=r'Invalid symbol "a" in quantifier braces. Only digits and a comma are allowed.',
    ):
        RegexTokenizer("a{1,a}")


def test_curly_brackets_empty():
    """
    Test that empty curly brackets (e.g., {}) raise a RegexTokenizerError.
    """
    with pytest.raises(
        RegexTokenizerError,
        match=r"Quantifier braces cannot be empty! Ensure the format is {n}, {n,}, or {n,m}.",
    ):
        RegexTokenizer("a{}")


def test_curly_brackets_with_extra_whitespace():
    """
    Test that a quantifier with extra whitespace (e.g., {1, 3}) raises a RegexTokenizerError.
    """
    with pytest.raises(
        RegexTokenizerError,
        match=r'Invalid symbol " " in quantifier braces. Only digits and a comma are allowed.',
    ):
        RegexTokenizer("a{1, 3}")


def test_curly_brackets_with_large_numbers():
    """
    Test that a quantifier with large numbers (e.g., {1000,2000}) is correctly tokenized.
    """
    sm = RegexTokenizer("a{1000,2000}")
    assert sm.tokens == ["a", "{1000,2000}"], "Failed to tokenize a quantifier with large numbers."


def test_curly_brackets_with_minimum_only():
    """
    Test that a quantifier with only a minimum value (e.g., {5,}) is correctly tokenized.
    """
    sm = RegexTokenizer("a{5,}")
    assert sm.tokens == ["a", "{5,}"], "Failed to tokenize a quantifier with only a minimum value."


def test_curly_brackets_with_exact_zero():
    """
    Test that a quantifier with an exact zero (e.g., {0}) is correctly tokenized.
    """
    sm = RegexTokenizer("a{0}")
    assert sm.tokens == ["a", "{0}"], "Failed to tokenize a quantifier with an exact zero."


def test_curly_brackets_with_zero_range():
    """
    Test that a quantifier with a zero range (e.g., {0,0}) is correctly tokenized.
    """
    sm = RegexTokenizer("a{0,0}")
    assert sm.tokens == ["a", "{0,0}"], "Failed to tokenize a quantifier with a zero range."


def test_curly_brackets_no_preceding_token():
    """
    Test that a quantifier (e.g., {1,3}) not preceded by a token raises a RegexTokenizerError.
    """
    with pytest.raises(
        RegexTokenizerError,
        match=r"Quantifier braces must be preceded, by a valid token.",
    ):
        RegexTokenizer("{1,3}")


def test_curly_brackets_invalid_preceding_token():
    """
    Test that a quantifier (e.g., {1,3}) not preceded by a valid token raises a RegexTokenizerError.
    """
    with pytest.raises(
        RegexTokenizerError,
        match=r"Quantifier braces must be preceded, by a valid token.",
    ):
        RegexTokenizer("${1,3}")


def test_curly_brackets_not_closed():
    """
    Test that unclosed quantifier braces raises a RegexTokenizerError.
    """
    with pytest.raises(
        UnclosedGroupError,
        match=r"Quantifier braces were not closed!",
    ):
        RegexTokenizer("a{1,3")


def test_curly_brackets_invalid_character_in_number():
    """
    Test that invalid characters in quantifier braces (e.g., {1a}) raise a RegexTokenizerError.
    """
    with pytest.raises(
        RegexTokenizerError,
        match=r'Invalid symbol "a" in quantifier braces. Only digits and a comma are allowed.',
    ):
        RegexTokenizer("a{1,a}")
