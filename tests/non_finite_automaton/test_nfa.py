"""
This is a test file for the Nondeterministic Finite Automaton (NFA) functionality.
"""

import pytest
from src.services.non_finite_automaton import (
    compile_regex,
    match_regex,
    InvalidRegexError,
    EmptyRegexError,
)


def test_compile_regex():
    """
    Test that the compilation of a postfix regex into an NFA is successful.
    """
    nfa = compile_regex("ab.c.")
    assert nfa.initial_state is not None, "Failed to create initial state for NFA."
    assert nfa.accept_state is not None, "Failed to create accept state for NFA."


def test_match_regex_basic_patterns():
    """
    Test that basic patterns are correctly matched by the NFA.
    """
    assert match_regex("a.b.c", "abc"), "Failed to match valid string for concatenation."
    assert not match_regex("a.b.c", "ab"), "Incorrectly matched invalid string for concatenation."


def test_match_regex_kleene_star():
    """
    Test that patterns with the Kleene star (*) are correctly matched by the NFA.
    """
    assert match_regex("a.b.c*", "ab"), "Failed to match valid string with Kleene star."
    assert match_regex("a.b.c*", "abc"), "Failed to match valid string with Kleene star."
    assert not match_regex("a.b.c*", "ac"), "Incorrectly matched invalid string with Kleene star."


def test_match_regex_alternation():
    """
    Test that patterns with alternation (|) are correctly matched by the NFA.
    """
    assert match_regex("a.(b|d).c", "abc"), "Failed to match valid string with alternation."
    assert match_regex("a.(b|d).c", "adc"), "Failed to match valid string with alternation."
    assert not match_regex(
        "a.(b|d).c", "aac"
    ), "Incorrectly matched invalid string with alternation."


def test_compile_regex_invalid():
    """
    Test that invalid regex patterns raise appropriate errors during compilation.
    """
    with pytest.raises(InvalidRegexError, match="Invalid regex: .*"):
        compile_regex("a|")


def test_compile_regex_empty():
    """
    Test that an empty regex raises an EmptyRegexError.
    """
    with pytest.raises(EmptyRegexError, match="The provided regex is empty."):
        compile_regex("")


def test_compile_regex_invalid_operator():
    """
    Test that invalid regex patterns raise InvalidRegexError.
    """
    with pytest.raises(InvalidRegexError, match="Invalid regex: \\* operator with no operand"):
        compile_regex("*")

    with pytest.raises(
        InvalidRegexError, match="Invalid regex: \\| operator requires two operands"
    ):
        compile_regex("a|")

    with pytest.raises(InvalidRegexError, match="Invalid regex: too many operands left on stack"):
        compile_regex("ab|c")


def test_match_regex_empty_string():
    """
    Test that an empty regex matches an empty string.
    """
    assert match_regex("", ""), "Failed to match empty regex with empty string."


def test_match_regex_literal():
    """
    Test that a regex with a single literal matches correctly.
    """
    assert match_regex("a", "a"), "Failed to match single literal."
    assert not match_regex("a", "b"), "Incorrectly matched different literal."


def test_match_regex_complex_patterns():
    """
    Test that complex regex patterns are matched correctly.
    """
    assert match_regex("a.b|c*", "ab"), "Failed to match valid string for complex pattern."
    assert match_regex("a.b|c*", "ccc"), "Failed to match valid string for Kleene star."
    assert not match_regex(
        "a.b|c*", "ac"
    ), "Incorrectly matched invalid string for complex pattern."


def test_compile_regex_invalid_characters():
    """
    Test that invalid characters in regex raise appropriate errors.
    """
    with pytest.raises(InvalidRegexError, match="Invalid regex: .*"):
        compile_regex("a[b")


def test_compile_regex_invalid_concatenation():
    """
    Test that invalid usage of the concatenation operator (.) raises InvalidRegexError.
    """
    with pytest.raises(InvalidRegexError, match="Invalid regex: .* operator requires two operands"):
        compile_regex("a.")

    with pytest.raises(InvalidRegexError, match="Invalid regex: .* operator requires two operands"):
        compile_regex(".a")


def test_compile_regex_invalid_plus_operator():
    """
    Test that invalid usage of the plus operator (+) raises InvalidRegexError.
    """
    with pytest.raises(InvalidRegexError, match="Invalid regex: \\+ operator with no operand"):
        compile_regex("+")


def test_compile_regex_invalid_question_operator():
    """
    Test that invalid usage of the question mark operator (?) raises InvalidRegexError.
    """
    with pytest.raises(InvalidRegexError, match="Invalid regex: \\? operator with no operand"):
        compile_regex("?")


def test_compile_regex_invalid_parentheses():
    """
    Test that parentheses in postfix notation raise InvalidRegexError.
    """
    with pytest.raises(
        InvalidRegexError, match="Parentheses should not appear in postfix notation."
    ):
        compile_regex("(")

    with pytest.raises(
        InvalidRegexError, match="Parentheses should not appear in postfix notation."
    ):
        compile_regex(")")


def test_match_regex_question_operator():
    """
    Test that patterns with the question mark (?) operator are correctly matched by the NFA.
    """
    assert match_regex("a.b?", "a"), "Failed to match valid string with ? operator."
    assert match_regex("a.b?", "ab"), "Failed to match valid string with ? operator."
    assert not match_regex("a.b?", "abb"), "Incorrectly matched invalid string with ? operator."


def test_match_regex_plus_operator():
    """
    Test that patterns with the plus (+) operator are correctly matched by the NFA.
    """
    assert match_regex("a.b+", "ab"), "Failed to match valid string with + operator."
    assert match_regex("a.b+", "abb"), "Failed to match valid string with + operator."
    assert not match_regex("a.b+", "a"), "Incorrectly matched invalid string with + operator."


def test_match_regex_empty_regex_error():
    """
    Test that an EmptyRegexError is raised when an empty regex is provided to matchRegex.
    """
    with pytest.raises(EmptyRegexError, match="The provided regex is empty."):
        match_regex("", "abc")
