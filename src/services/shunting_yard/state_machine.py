r"""
Cheat Sheet

Character classes
.	any character except newline            ✅
\w \d \s	word, digit, whitespace         ✅
\W \D \S	not word, digit, whitespace     ✅
[abc]	any of a, b, or c                   ✅
[^abc]	not a, b, or c                      ✅
[a-g]	character between a & g             ✅

Anchors
^abc$	start / end of the string
\b	word boundary                           ✅

Escaped characters
\. \* \\	escaped special characters      ✅
\t \n \r	tab, linefeed, carriage return  ✅
\u00a9	unicode escaped ©                   ✅

Groups & Lookaround
(abc)	capture group
\1	backreference to group #1               ✅
(?:abc)	non-capturing group
(?=abc)	positive lookahead
(?!abc)	negative lookahead

Quantifiers & Alternation
a* a+ a?	0 or more, 1 or more, 0 or 1
a{5} a{2,}	exactly five, two or more
a{1,3}	between one & three
a+? a{2,}?	match as few as possible
ab|cd	match ab or cd
"""

import string
from enum import Enum
from itertools import islice
from .exceptions import (
    StateMachineError,
    EscapeSequenceEndError,
    EscapeSequenceLengthError,
    EndsWithBackslashError,
    UnclosedGroupError,
)


class UnicodeEscapeLength(Enum):
    """
    This is the total length of the escaped unicode string
    including the x/u/U, and the backslash "\\"
    """

    STANDARD_ESCAPE_LENGTH = 2  # e.g. \n, \\
    HEX = 4  # e.g. \xXX
    UNICODE_SHORT = 6  # e.g. \uXXXX
    UNICODE_LONG = 10  # e.g. \UXXXXXXXX


class TokenTypes(Enum):
    LITERAL = "Literal"
    ESCAPE_SEQUENCE = "Escape Sequence"
    CHARACTER_CLASS = "Character Class"
    CAPTURE_GROUP = "Capture Group"
    QUANTIFIER = "Quantifier"
    DOT = "Dot"
    SPECIAL = "Special Symbol"


class StateMachine:
    """
    This is a state machine.
    \\ escapes the special character after it.
    ^ is always accepted as in the start of a string it is an achor and otherwise it's a literal.
    $ likewise, except end of a string.
    +*?| are also literals when not in a specific location.
    """

    def __init__(self, input_string: str):
        self.__input_string = input_string
        self.i = 0
        self.symbol: str = None
        self.tokens = []
        self.token_types = []
        self.input_string_length = len(input_string)
        self.literals = string.ascii_letters + "." + string.digits
        self.special_symbols = "$^+*?|"
        self.unconditional_characters = self.literals + self.special_symbols
        self.input_iterable = iter(enumerate(self.input_string))
        self.quantifier_allowed_preceding_token_types = [
            TokenTypes.LITERAL,
            TokenTypes.CHARACTER_CLASS,
            TokenTypes.CAPTURE_GROUP,
            TokenTypes.DOT,
            TokenTypes.ESCAPE_SEQUENCE,
        ]

    @property
    def input_string(self):
        """Read-only property for input_string."""
        return self.__input_string

    def tokenize(self):
        """
        Divide the input into tokens.
        """
        while True:
            try:
                self.i, self.symbol = next(self.input_iterable)

                match self.symbol:
                    case "\\":
                        self.tokens.append(self.__handle_escape_sequence())
                        self.token_types.append(TokenTypes.ESCAPE_SEQUENCE)

                    case "[":
                        self.tokens.append(self.__handle_square_brackets())
                        self.token_types.append(TokenTypes.CHARACTER_CLASS)

                    case "{":
                        if (
                            self.token_types[-1]
                            not in self.quantifier_allowed_preceding_token_types
                        ):
                            raise StateMachineError(
                                "Quantifier braces must be preceded, by a valid token."
                            )
                        self.tokens.append(self.__handle_curly_brackets())
                        self.token_types.append(TokenTypes.QUANTIFIER)

                    case "(":
                        self.tokens.append(self.__handle_capture_group())
                        self.token_types.append(TokenTypes.CAPTURE_GROUP)

                    case _ if self.symbol in self.literals:
                        self.tokens.append(self.symbol)
                        self.token_types.append(TokenTypes.LITERAL)

                    case _ if self.symbol in self.special_symbols:
                        self.tokens.append(self.symbol)
                        self.token_types.append(TokenTypes.SPECIAL)

                    case _:
                        raise NotImplementedError(f"Unrecognized symbol: {self.symbol}")

            except StopIteration:
                break

        print(f"input string: {self.input_string} fully tokenized:\n{self.tokens}")

    def __progress_iterable(self, amount: int):
        """
        skip the rest of the token before continuing to process the input string.
        """
        self.input_iterable = islice(self.input_iterable, amount, None)
        self.i += amount

    def __handle_escape_sequence(self):
        """
        Implementation:
        backslash "\\" starts an escape sequence, in most cases the total length is 2,
        but when it is followed by an "x", a "u" or a capital "U",
        the escape sequence length becomes 4, 6, or 10 respectively,
        to accomodate for the appropriate length unicode character
        representation.
        In this implementation any character following a backslash apart from
        the afore mentioned exceptions is considered a valid escaped sequence.
        """

        escape_sequence_lengths = {
            "x": UnicodeEscapeLength.HEX.value,
            "u": UnicodeEscapeLength.UNICODE_SHORT.value,
            "U": UnicodeEscapeLength.UNICODE_LONG.value,
        }
        escape_sequence_length = None

        try:
            escape_sequence_length = escape_sequence_lengths.get(
                escape_type := self.input_string[self.i + 1],  # defining the escape type
                UnicodeEscapeLength.STANDARD_ESCAPE_LENGTH.value,
            )

            # Validate escape sequence characters
            if escape_sequence_length >= UnicodeEscapeLength.HEX.value:
                if not all(
                    char in string.hexdigits
                    for char in self.input_string[self.i : self.i + escape_sequence_length]
                ):
                    raise StateMachineError(
                        f'Invalid escape sequence "\\{self.input_string[self.i : self.i + escape_sequence_length]}" '
                        f"at index {self.i}. Expected hexadecimal characters."
                    )

            # build the token
            token = self.input_string[self.i : self.i + escape_sequence_length]

            # Validate the length of the escape sequence
            if len(token) < escape_sequence_length:
                raise EscapeSequenceLengthError(
                    f'Incomplete escape sequence "\\{escape_type}" at index {self.i}. '
                    f"Expected length: {escape_sequence_length}, but got {len(token)}."
                    f"Input: {self.input_string}\n"
                    f"{' ' * (7 + self.i)}{'^' * len(token)}"
                )

            self.__progress_iterable(escape_sequence_length - 1)

            return token

        except IndexError as exc:
            if not escape_sequence_length:
                raise EndsWithBackslashError('input string cannot end in a backslash "\\"') from exc
            raise EscapeSequenceEndError(
                f'Unexpected end of input for escape sequence "\\{escape_type}" at index {self.i}. '
                f"Expected length: {escape_sequence_length}."
                f"Input: {self.input_string}\n"
                f"{' ' * (7 + self.i)}{'^' * len(token)}"
            ) from exc

    def __handle_square_brackets(self):
        """
        implemetation:
        all unconditional characters allowed,
        "]" only allowed if preceded by a backslash "\\"
        "[" always allowed
        otherwise will end the set
        "^" only special at the beginning
        "[^]" not allowed
        "-" special between "independent" characters
        "-" non-special at the beginning or end, or after a backslash
        same rules for "\\" as generally
        """
        valid_lowercase_ranges = string.ascii_lowercase
        valid_uppercase_ranges = string.ascii_uppercase
        valid_number_ranges = string.digits
        valid_range_characters = (
            valid_number_ranges + valid_lowercase_ranges + valid_uppercase_ranges
        )

        token = self.symbol
        nonindependent_character_indices = []

        i = 0
        while True:
            try:
                self.i, symbol = next(self.input_iterable)
                i += 1
                match symbol:

                    case "\\":
                        token += self.__handle_escape_sequence()

                    case "^":
                        if i == 1:  # first character in set
                            if self.input_string[self.i + 1] != "]":
                                token += symbol
                            else:
                                raise StateMachineError(
                                    '"^" cannot be the only character in a character set!'
                                )
                        else:
                            token += symbol

                    case "-":
                        # Handle ranges (e.g., a-z)
                        self.i, next_symbol = next(self.input_iterable)
                        if next_symbol == "]":
                            # Treat "-" as a literal if it's the last character
                            token += symbol
                            token += next_symbol
                            break
                        if len(token) > 1 and token[-1] != "[":
                            # Ensure "-" is between two valid characters
                            if (
                                token[-1] in valid_range_characters
                                and next_symbol in valid_range_characters
                            ):
                                # Check if the range is valid and not already used
                                if (
                                    (
                                        token[-1] in valid_lowercase_ranges
                                        and next_symbol in valid_lowercase_ranges
                                        and valid_lowercase_ranges.index(token[-1])
                                        < valid_lowercase_ranges.index(next_symbol)
                                    )
                                    or (
                                        token[-1] in valid_uppercase_ranges
                                        and next_symbol in valid_uppercase_ranges
                                        and valid_uppercase_ranges.index(token[-1])
                                        < valid_uppercase_ranges.index(next_symbol)
                                    )
                                    or (
                                        token[-1] in valid_number_ranges
                                        and next_symbol in valid_number_ranges
                                        and valid_number_ranges.index(token[-1])
                                        < valid_number_ranges.index(next_symbol)
                                    )
                                ):
                                    # Append the valid range
                                    if (
                                        self.i - 2 in nonindependent_character_indices
                                        or self.i in nonindependent_character_indices
                                    ):
                                        raise StateMachineError(
                                            f"Invalid range: '{token[-1]}-{next_symbol}' uses a range character with an already used range."
                                        )
                                    nonindependent_character_indices.extend([self.i - 2, self.i])
                                    token += symbol
                                    token += next_symbol
                                else:
                                    raise StateMachineError(
                                        f"Invalid range: '{token[-1]}-{next_symbol}' is not a valid range."
                                    )
                            else:
                                # Treat "-" as a literal if it's not part of a valid range
                                token += symbol
                                token += next_symbol
                        else:
                            # Treat "-" as a literal if it's at the start
                            token += symbol
                            token += next_symbol

                    case _ if symbol in self.unconditional_characters:
                        token += symbol

                    case "]":
                        token += symbol
                        break

            except StopIteration as exc:
                raise UnclosedGroupError("Squarebracket character set was not closed!") from exc

            except IndexError as exc:
                raise UnclosedGroupError("Squarebracket character set was not closed!") from exc

        return token

    def __handle_curly_brackets(self):
        """
        Implementation:
        Cheat Sheet:
        a{5} a{2,}	exactly five, two or more
        a{1,3}	between one & three
        a+? a{2,}?	match as few as possible
        """

        token = self.symbol
        comma_used = False
        previous_number = None
        while True:
            try:
                self.i, symbol = next(self.input_iterable)

                match symbol:

                    case "}":
                        if len(token) == 1:
                            raise StateMachineError(
                                "Quantifier braces cannot be empty! Ensure the format is {n}, {n,}, or {n,m}."
                            )
                        token += symbol
                        break

                    case ",":
                        if comma_used:
                            raise StateMachineError(
                                "Quantifier braces cannot include multiple commas!"
                            )

                        if previous_number == None:
                            raise StateMachineError(
                                "Quantifier braces cannot start with a comma! Ensure the format is {n} or {n,m}."
                            )

                        comma_used = True
                        token += symbol

                    case _ if symbol in string.digits:
                        number = self.__get_number(symbol)
                        if comma_used:
                            if previous_number and previous_number >= number:
                                raise StateMachineError(
                                    "Range specified in quantifier braces must be rising!"
                                )
                        token += str(number)
                        previous_number = number

                    case _:
                        raise StateMachineError(
                            f'Invalid symbol "{symbol}" in quantifier braces. Only digits and a comma are allowed.'
                        )

            except StopIteration as exc:
                raise UnclosedGroupError("Quantifier braces were not closed!") from exc

        return token

    def __get_number(self, initial_digit: str) -> int:
        """
        Extracts the next number from the input string within quantifier braces.

        Args:
            initial_digit (str): The first digit of the number.

        Returns:
            int: The complete number parsed from the input.

        Raises:
            UnclosedGroupError: If the quantifier braces are not properly closed.
            StateMachineError: If an invalid symbol is encountered in the braces.
        """
        digits = [initial_digit]
        i = self.i
        while i + 1 < self.input_string_length:
            i += 1
            symbol = self.input_string[i]

            if symbol in ",}":
                break

            if symbol not in string.digits:
                raise StateMachineError(
                    f'Invalid symbol "{symbol}" in quantifier braces. Only digits and a comma are allowed.'
                )

            self.i, _ = next(self.input_iterable)
            digits.append(symbol)

        else:
            raise UnclosedGroupError("Quantifier braces were not closed!")

        return int("".join(digits))

    def __handle_capture_group(self):
        """
        Implementation:
        All characters inside a capture group are considered valid.
        Capture group is considered valid as long as it doesn't end in a backslash "\\"
        """

        token = self.symbol

        i = 0
        while True:
            try:
                self.i, symbol = next(self.input_iterable)
                i += 1

                match symbol:

                    case "\\":
                        token += self.__handle_escape_sequence()

                    case "(":
                        token += self.__handle_capture_group()

                    case ")":
                        token += symbol
                        break

                    case _:
                        token += symbol

            except StopIteration as exc:
                raise UnclosedGroupError("Capture Group was not closed!") from exc

            except Exception as exc:
                raise NotImplementedError("Unexpected error occurred!") from exc

        return token


if __name__ == "__main__":
    pass
