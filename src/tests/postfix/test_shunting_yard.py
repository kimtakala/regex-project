"""
This is a test file for the shunting yard algorithm.
"""

import pytest
from src.services.postfix.postfix import shunting_yard


def test_shunting_yard_concatenation():
    """
    Test that the shunting yard algorithm correctly converts concatenation.
    """
    assert (
        shunting_yard("a.b.c") == "ab.c."
    ), "Failed to convert infix to postfix for concatenation."


def test_shunting_yard_alternation():
    """
    Test that the shunting yard algorithm correctly converts alternation.
    """
    assert shunting_yard("a|b") == "ab|", "Failed to convert infix to postfix for alternation."


def test_shunting_yard_grouping_and_kleene_star():
    """
    Test that the shunting yard algorithm correctly converts grouping and Kleene star.
    """
    assert (
        shunting_yard("(a.b)*") == "ab.*"
    ), "Failed to convert infix to postfix for grouping and Kleene star."


def test_shunting_yard_mismatched_parentheses():
    """
    Test that the shunting yard algorithm raises MismatchedParenthesesError for mismatched parentheses.
    """
    with pytest.raises(Exception, match="Mismatched parentheses: '\\)' without matching '\\('"):
        shunting_yard("a.b)")
    with pytest.raises(Exception, match="Mismatched parentheses: '\\(' without matching '\\)'"):
        shunting_yard("(a.b")


def test_shunting_yard_empty_input():
    """
    Test that the shunting yard algorithm handles empty input correctly.
    """
    assert shunting_yard("") == "", "Failed to handle empty input."


def test_shunting_yard_single_character():
    """
    Test that the shunting yard algorithm handles a single character correctly.
    """
    assert shunting_yard("a") == "a", "Failed to handle single character input."


def test_shunting_yard_multiple_operators():
    """
    Test that the shunting yard algorithm handles multiple operators correctly.
    """
    assert shunting_yard("a|b.c*") == "ab|c.*", "Failed to handle multiple operators."


def test_shunting_yard_invalid_input():
    """
    Test that the shunting yard algorithm raises an error for invalid input.
    """
    with pytest.raises(Exception, match="Mismatched parentheses: .*"):
        shunting_yard("(a|b")
