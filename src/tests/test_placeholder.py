import pytest
from src import StateMachine


def test_escape_sequence():
    sm = StateMachine("\\a")
    sm.tokenize(sm.input_string)
    assert sm.tokens == ["\\a"], "Failed to correctly tokenize an escape sequence."


def test_unconditional_characters():
    sm = StateMachine(".")
    sm.tokenize(sm.input_string)
    assert sm.tokens == [], "Failed to ignore unconditional characters."


def test_caret_at_start():
    sm = StateMachine("^")
    sm.tokenize(sm.input_string)
    assert sm.tokens == [], "Caret at the start should not be tokenized."


def test_caret_inside():
    sm = StateMachine("a^b")
    sm.tokenize(sm.input_string)
    assert sm.tokens == ["^"], "Caret inside the string should be tokenized."


def test_dollar_at_end():
    sm = StateMachine("a$")
    sm.tokenize(sm.input_string)
    assert sm.tokens == [], "Dollar at the end should not be tokenized."


def test_dollar_inside():
    sm = StateMachine("a$b")
    sm.tokenize(sm.input_string)
    assert sm.tokens == ["$"], "Dollar inside the string should be tokenized."


def test_backslash_at_end():
    sm = StateMachine("a\\")
    with pytest.raises(ValueError, match=r"Can't end with a backslash character \""):
        sm.tokenize(sm.input_string)


def test_ignored_characters():
    sm = StateMachine("[*+?{]")
    sm.tokenize(sm.input_string)
    assert sm.tokens == [], "Ignored characters should not be tokenized."


def test_mixed_input():
    sm = StateMachine("a^b$c.d\\e")
    sm.tokenize(sm.input_string)
    assert sm.tokens == [
        "^",
        "$",
        "\\e",
    ], "Tokenization result is incorrect for mixed input."


if __name__ == "__main__":
    pytest.main()
