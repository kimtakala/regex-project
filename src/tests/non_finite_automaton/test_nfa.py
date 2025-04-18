"""
This is a test file for the Nondeterministic Finite Automaton (NFA) functionality.
"""

import pytest
from src.services.non_finite_automaton.nfa import compileRegex, matchRegex
from src.services.non_finite_automaton.exceptions import InvalidRegexError, EmptyRegexError


def test_compile_regex():
    """
    Test that the compilation of a postfix regex into an NFA is successful.
    """
    nfa = compileRegex("ab.c.")
    assert nfa.initial_state is not None, "Failed to create initial state for NFA."
    assert nfa.accept_state is not None, "Failed to create accept state for NFA."


def test_match_regex_basic_patterns():
    """
    Test that basic patterns are correctly matched by the NFA.
    """
    assert matchRegex("a.b.c", "abc"), "Failed to match valid string for concatenation."
    assert not matchRegex("a.b.c", "ab"), "Incorrectly matched invalid string for concatenation."


def test_match_regex_kleene_star():
    """
    Test that patterns with the Kleene star (*) are correctly matched by the NFA.
    """
    assert matchRegex("a.b.c*", "ab"), "Failed to match valid string with Kleene star."
    assert matchRegex("a.b.c*", "abc"), "Failed to match valid string with Kleene star."
    assert not matchRegex("a.b.c*", "ac"), "Incorrectly matched invalid string with Kleene star."


def test_match_regex_alternation():
    """
    Test that patterns with alternation (|) are correctly matched by the NFA.
    """
    assert matchRegex("a.(b|d).c", "abc"), "Failed to match valid string with alternation."
    assert matchRegex("a.(b|d).c", "adc"), "Failed to match valid string with alternation."
    assert not matchRegex(
        "a.(b|d).c", "aac"
    ), "Incorrectly matched invalid string with alternation."


def test_compile_regex_invalid():
    """
    Test that invalid regex patterns raise appropriate errors during compilation.
    """
    with pytest.raises(InvalidRegexError, match="Invalid regex: .*"):
        compileRegex("a|")


def test_compile_regex_empty():
    """
    Test that an empty regex raises an EmptyRegexError.
    """
    with pytest.raises(EmptyRegexError, match="The provided regex is empty."):
        compileRegex("")


def test_compile_regex_invalid_operator():
    """
    Test that invalid regex patterns raise InvalidRegexError.
    """
    with pytest.raises(InvalidRegexError, match="Invalid regex: \\* operator with no operand"):
        compileRegex("*")

    with pytest.raises(
        InvalidRegexError, match="Invalid regex: \\| operator requires two operands"
    ):
        compileRegex("a|")

    with pytest.raises(InvalidRegexError, match="Invalid regex: too many operands left on stack"):
        compileRegex("ab|c")


def test_match_regex_empty_string():
    """
    Test that an empty regex matches an empty string.
    """
    assert matchRegex("", ""), "Failed to match empty regex with empty string."


def test_match_regex_literal():
    """
    Test that a regex with a single literal matches correctly.
    """
    assert matchRegex("a", "a"), "Failed to match single literal."
    assert not matchRegex("a", "b"), "Incorrectly matched different literal."


def test_match_regex_complex_patterns():
    """
    Test that complex regex patterns are matched correctly.
    """
    assert matchRegex("a.b|c*", "ab"), "Failed to match valid string for complex pattern."
    assert matchRegex("a.b|c*", "ccc"), "Failed to match valid string for Kleene star."
    assert not matchRegex("a.b|c*", "ac"), "Incorrectly matched invalid string for complex pattern."


def test_compile_regex_invalid_characters():
    """
    Test that invalid characters in regex raise appropriate errors.
    """
    with pytest.raises(InvalidRegexError, match="Invalid regex: .*"):
        compileRegex("a[b")
