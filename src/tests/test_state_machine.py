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


def test_escape_sequence():
    """
    Test that escape sequences (e.g., \n) are correctly tokenized.
    """
    sm = StateMachine("\\n")
    sm.tokenize()
    assert sm.tokens == ["\\n"], "Failed to correctly tokenize an escape sequence."


def test_incomplete_escape_sequence():
    """
    Test that incomplete escape sequences raise a StateMachineError.
    """
    sm = StateMachine("\\x1")
    with pytest.raises(
        StateMachineError,
        match=r'Invalid escape sequence "\\\\x1" at index 0. Expected hexadecimal characters.',
    ):
        sm.tokenize()


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


def test_square_brackets_simple():
    """
    Test that simple character sets (e.g., [abc]) are correctly tokenized.
    """
    sm = StateMachine("[abc]")
    sm.tokenize()
    assert sm.tokens == ["[abc]"], "Failed to tokenize a simple character set."


def test_square_brackets_with_caret():
    """
    Test that negated character sets (e.g., [^abc]) are correctly tokenized.
    """
    sm = StateMachine("[^abc]")
    sm.tokenize()
    assert sm.tokens == ["[^abc]"], "Failed to tokenize a negated character set."


def test_square_brackets_with_dash():
    """
    Test that character ranges (e.g., [a-z]) are correctly tokenized.
    """
    sm = StateMachine("[a-z]")
    sm.tokenize()
    assert sm.tokens == ["[a-z]"], "Failed to tokenize a character range."


def test_square_brackets_unclosed():
    """
    Test that unclosed square brackets raise a UnclosedGroupError.
    """
    sm = StateMachine("[abc")
    with pytest.raises(UnclosedGroupError, match=r"Squarebracket character set was not closed!"):
        sm.tokenize()


def test_backslash_at_end():
    """
    Test that a backslash at the end of the input string raises a EndsWithBackslashError.
    """
    sm = StateMachine("abc\\")
    with pytest.raises(
        EndsWithBackslashError, match=re.escape('input string cannot end in a backslash "\\"')
    ):
        sm.tokenize()


def test_invalid_range_in_square_brackets():
    """
    Test that invalid ranges in square brackets (e.g., [a-b-c]) raise a StateMachineError.
    """
    sm = StateMachine("[a-b-c]")
    with pytest.raises(
        StateMachineError,
        match=r"Invalid range: 'b-c' uses a range character with an already used range.",
    ):
        sm.tokenize()


def test_square_brackets_with_escape_sequence():
    """
    Test that square brackets containing escape sequences (e.g., [a\\z]) are correctly tokenized.
    """
    sm = StateMachine("[a\\z]")
    sm.tokenize()
    assert sm.tokens == ["[a\\z]"], "Failed to tokenize square brackets with an escaped backslash."


def test_square_brackets_with_literal_dash():
    """
    Test that square brackets containing a literal dash (e.g., [-abc]) are correctly tokenized.
    """
    sm = StateMachine("[-abc]")
    sm.tokenize()
    assert sm.tokens == ["[-abc]"], "Failed to tokenize square brackets with a literal dash."


def test_capture_group_simple():
    """
    Test that a simple capture group (e.g., (abc)) is correctly tokenized.
    """
    sm = StateMachine("(abc)")
    sm.tokenize()
    assert sm.tokens == ["(abc)"], "Failed to tokenize a simple capture group."


def test_capture_group_with_escape_sequence():
    """
    Test that a capture group containing an escape sequence (e.g., (a\\n)) is correctly tokenized.
    """
    sm = StateMachine("(a\\n)")
    sm.tokenize()
    assert sm.tokens == ["(a\\n)"], "Failed to tokenize a capture group with an escape sequence."


def test_capture_group_unclosed():
    """
    Test that an unclosed capture group (e.g., (abc) raises a UnclosedGroupError.
    """
    sm = StateMachine("(abc")
    with pytest.raises(UnclosedGroupError, match=r"Capture Group was not closed!"):
        sm.tokenize()


def test_capture_group_with_nested_parentheses():
    """
    Test that a capture group with nested parentheses (e.g., (a(b)c)) is correctly tokenized.
    """
    sm = StateMachine("(a(b)c)")
    sm.tokenize()
    assert sm.tokens == ["(a(b)c)"], "Failed to tokenize a capture group with nested parentheses."


def test_capture_group_with_special_characters():
    """
    Test that a capture group containing special characters (e.g., (a+b*c?)) is correctly tokenized.
    """
    sm = StateMachine("(a+b*c?)")
    sm.tokenize()
    assert sm.tokens == ["(a+b*c?)"], "Failed to tokenize a capture group with special characters."


def test_capture_group_with_backslash_at_end():
    """
    Test that a capture group ending with a backslash (e.g., (abc\\)) raises a UnclosedGroupError.
    """
    sm = StateMachine("(abc\\)")
    with pytest.raises(UnclosedGroupError, match=r"Capture Group was not closed!"):
        sm.tokenize()


def test_curly_brackets_exact_number():
    """
    Test that a quantifier with an exact number (e.g., {5}) is correctly tokenized.
    """
    sm = StateMachine("a{5}")
    sm.tokenize()
    assert sm.tokens == ["a", "{5}"], "Failed to tokenize a quantifier with an exact number."


def test_curly_brackets_minimum_number():
    """
    Test that a quantifier with a minimum number (e.g., {2,}) is correctly tokenized.
    """
    sm = StateMachine("a{2,}")
    sm.tokenize()
    assert sm.tokens == ["a", "{2,}"], "Failed to tokenize a quantifier with a minimum number."


def test_curly_brackets_range():
    """
    Test that a quantifier with a range (e.g., {1,3}) is correctly tokenized.
    """
    sm = StateMachine("a{1,3}")
    sm.tokenize()
    assert sm.tokens == ["a", "{1,3}"], "Failed to tokenize a quantifier with a range."


def test_curly_brackets_unclosed():
    """
    Test that an unclosed quantifier (e.g., {5) raises a UnclosedGroupError.
    """
    sm = StateMachine("a{5")
    with pytest.raises(UnclosedGroupError, match=r"Quantifier braces were not closed!"):
        sm.tokenize()


def test_curly_brackets_multiple_commas():
    """
    Test that a quantifier with multiple commas (e.g., {1,3,}) raises a StateMachineError.
    """
    sm = StateMachine("a{1,3,}")
    with pytest.raises(
        StateMachineError, match=r"Quantifier braces cannot include multiple commas!"
    ):
        sm.tokenize()


def test_curly_brackets_start_with_comma():
    """
    Test that a quantifier starting with a comma (e.g., {,5}) raises a StateMachineError.
    """
    sm = StateMachine("a{,5}")
    with pytest.raises(
        StateMachineError,
        match=r"Quantifier braces cannot start with a comma! Ensure the format is {n} or {n,m}.",
    ):
        sm.tokenize()


def test_curly_brackets_non_rising_range():
    """
    Test that a quantifier with a non-rising range (e.g., {3,1}) raises a StateMachineError.
    """
    sm = StateMachine("a{3,1}")
    with pytest.raises(
        StateMachineError, match=r"Range specified in quantifier braces must be rising!"
    ):
        sm.tokenize()


def test_curly_brackets_invalid_character():
    """
    Test that a quantifier with invalid characters (e.g., {1,a}) raises a StateMachineError.
    """
    sm = StateMachine("a{1,a}")
    with pytest.raises(
        StateMachineError,
        match=r'Invalid symbol "a" in quantifier braces. Only digits and a comma are allowed.',
    ):
        sm.tokenize()


def test_curly_brackets_empty():
    """
    Test that empty curly brackets (e.g., {}) raise a StateMachineError.
    """
    sm = StateMachine("a{}")
    with pytest.raises(
        StateMachineError,
        match=r"Quantifier braces cannot be empty! Ensure the format is {n}, {n,}, or {n,m}.",
    ):
        sm.tokenize()


def test_curly_brackets_with_extra_whitespace():
    """
    Test that a quantifier with extra whitespace (e.g., {1, 3}) raises a StateMachineError.
    """
    sm = StateMachine("a{1, 3}")
    with pytest.raises(
        StateMachineError,
        match=r'Invalid symbol " " in quantifier braces. Only digits and a comma are allowed.',
    ):
        sm.tokenize()


def test_curly_brackets_with_large_numbers():
    """
    Test that a quantifier with large numbers (e.g., {1000,2000}) is correctly tokenized.
    """
    sm = StateMachine("a{1000,2000}")
    sm.tokenize()
    assert sm.tokens == ["a", "{1000,2000}"], "Failed to tokenize a quantifier with large numbers."


def test_curly_brackets_with_minimum_only():
    """
    Test that a quantifier with only a minimum value (e.g., {5,}) is correctly tokenized.
    """
    sm = StateMachine("a{5,}")
    sm.tokenize()
    assert sm.tokens == ["a", "{5,}"], "Failed to tokenize a quantifier with only a minimum value."


def test_curly_brackets_with_exact_zero():
    """
    Test that a quantifier with an exact zero (e.g., {0}) is correctly tokenized.
    """
    sm = StateMachine("a{0}")
    sm.tokenize()
    assert sm.tokens == ["a", "{0}"], "Failed to tokenize a quantifier with an exact zero."


def test_curly_brackets_with_zero_range():
    """
    Test that a quantifier with a zero range (e.g., {0,0}) is correctly tokenized.
    """
    sm = StateMachine("a{0,0}")
    sm.tokenize()
    assert sm.tokens == ["a", "{0,0}"], "Failed to tokenize a quantifier with a zero range."


if __name__ == "__main__":
    pytest.main()
