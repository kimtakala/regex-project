"""
Tests for special symbols and other characters in RegexTokenizer.
"""

import pytest
from src.services.regex_search.regex_tokenizer import RegexTokenizer


def test_special_symbols():
    """
    Test that special symbols (e.g., ^, $, |) are correctly tokenized.
    """
    sm = RegexTokenizer("^$|")
    assert sm.tokens == ["^", "$", "|"], "Failed to tokenize special symbols."


def test_other_characters():
    """
    Test that other characters (e.g., @, #, &) are correctly tokenized.
    """
    sm = RegexTokenizer("@#&")
    assert sm.tokens == ["@", "#", "&"], "Failed to tokenize other characters."
