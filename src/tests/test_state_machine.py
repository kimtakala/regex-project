"""
This is a test file for the StateMachine.
"""

import pytest
from src import StateMachine


def test_escape_sequence():
    """
    Test that escape sequences (e.g., \n) are correctly tokenized.
    """
    sm = StateMachine("\\n")
    sm.tokenize()
    assert sm.tokens == ["\\n"], "Failed to correctly tokenize an escape sequence."


def test_incomplete_escape_sequence():
    """
    Test that incomplete escape sequences raise a ValueError.
    """
    sm = StateMachine("\\x1")
    with pytest.raises(ValueError, match=r"Incomplete escape sequence"):
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
    Test that unclosed square brackets raise a ValueError.
    """
    sm = StateMachine("[abc")
    with pytest.raises(ValueError, match=r"Squarebracket character set was not closed!"):
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
    Test that a backslash at the end of the input string raises a ValueError.
    """
    sm = StateMachine("abc\\")
    with pytest.raises(ValueError, match=r"input string cannot end in a backslash"):
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
    Test that invalid ranges in square brackets (e.g., [a-b-c]) raise a ValueError.
    """
    sm = StateMachine("[a-b-c]")
    with pytest.raises(
        ValueError,
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


if __name__ == "__main__":
    pytest.main()
