import pytest
from src import StateMachine
from . import (
    StateMachineError,
    EndsWithBackslashError,
    EscapeSequenceEndError,
    EscapeSequenceLengthError,
    UnclosedGroupError,
)


def test_square_brackets_simple():
    """
    Test that simple character sets (e.g., [abc]) are correctly tokenized.
    """
    sm = StateMachine("[abc]")
    assert sm.tokens == ["[abc]"], "Failed to tokenize a simple character set."


def test_square_brackets_with_caret():
    """
    Test that negated character sets (e.g., [^abc]) are correctly tokenized.
    """
    sm = StateMachine("[^abc]")
    assert sm.tokens == ["[^abc]"], "Failed to tokenize a negated character set."


def test_square_brackets_with_dash():
    """
    Test that character ranges (e.g., [a-z]) are correctly tokenized.
    """
    sm = StateMachine("[a-z]")
    assert sm.tokens == ["[a-z]"], "Failed to tokenize a character range."


def test_square_brackets_unclosed():
    """
    Test that unclosed square brackets raise a UnclosedGroupError.
    """
    with pytest.raises(UnclosedGroupError, match=r"Squarebracket character set was not closed!"):
        StateMachine("[abc")


def test_invalid_range_in_square_brackets():
    """
    Test that invalid ranges in square brackets (e.g., [a-b-c]) raise a StateMachineError.
    """
    with pytest.raises(
        StateMachineError,
        match=r"Invalid range: 'b-c' uses a range character with an already used range.",
    ):
        StateMachine("[a-b-c]")


def test_square_brackets_with_escape_sequence():
    """
    Test that square brackets containing escape sequences (e.g., [a\\z]) are correctly tokenized.
    """
    sm = StateMachine("[a\\z]")
    assert sm.tokens == ["[a\\z]"], "Failed to tokenize square brackets with an escaped backslash."


def test_square_brackets_with_literal_dash():
    """
    Test that square brackets containing a literal dash (e.g., [-abc]) are correctly tokenized.
    """
    sm = StateMachine("[-abc]")
    assert sm.tokens == ["[-abc]"], "Failed to tokenize square brackets with a literal dash."
