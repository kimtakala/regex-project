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


# def test_caret_at_start():
#     sm = StateMachine("^abc")
#     sm.tokenize()
#     assert sm.tokens == ["^abc"], "Failed to tokenize caret at the start."


# def test_caret_inside():
#     sm = StateMachine("a^b")
#     sm.tokenize()
#     assert sm.tokens == ["a", "^", "b"], "Failed to tokenize caret inside the string."


# def test_dollar_at_end():
#     sm = StateMachine("abc$")
#     sm.tokenize()
#     assert sm.tokens == ["abc"], "Failed to handle dollar at the end."


# def test_dollar_inside():
#     sm = StateMachine("a$b")
#     sm.tokenize()
#     assert sm.tokens == ["a", "$", "b"], "Failed to tokenize dollar inside the string."


def test_backslash_at_end():
    """
    Test that a backslash at the end of the input string raises a EndsWithBackslashError.
    """
    sm = StateMachine("abc\\")
    with pytest.raises(
        EndsWithBackslashError, match=re.escape('input string cannot end in a backslash "\\"')
    ):
        sm.tokenize()


# def test_mixed_input():
#     sm = StateMachine("a^b$c.d\\e[f-g]")
#     sm.tokenize()
#     assert sm.tokens == [
#         "a",
#         "^",
#         "b",
#         "$",
#         "c",
#         ".",
#         "d",
#         "\\e",
#         "[f-g]",
#     ], "Failed to tokenize mixed input."


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


if __name__ == "__main__":
    pytest.main()
