"""
This module defines a RegexTokenizer class for handling regex syntax and splitting it into tokens.
"""

import string
from enum import Enum
from itertools import islice
from .exceptions import (
    RegexTokenizerError,
    EscapeSequenceLengthError,
    EndsWithBackslashError,
    UnclosedGroupError,
)


# Enum for defining the lengths of various Unicode escape sequences
class UnicodeEscapeLength(Enum):
    """
    Enum representing the total length of various Unicode escape sequences.
    This includes the backslash "\\\\" and the escape type (e.g., "x", "u", "U").
    It is used to validate and process escape sequences in the input string.

    Attributes:
        STANDARD_ESCAPE_LENGTH: Length of standard escape sequences (e.g., \\n, \\\).
        HEX: Length of hexadecimal escape sequences (e.g., \\xXX).
        UNICODE_SHORT: Length of short Unicode escape sequences (e.g., \\uXXXX).
        UNICODE_LONG: Length of long Unicode escape sequences (e.g., \\UXXXXXXXX).
    """

    STANDARD_ESCAPE_LENGTH = 2  # e.g. \n, \\
    HEX = 4  # e.g. \xXX
    UNICODE_SHORT = 6  # e.g. \uXXXX
    UNICODE_LONG = 10  # e.g. \UXXXXXXXX


# Enum for defining different token types in a regular expression
class TokenTypes(Enum):
    """
    Enum representing the different types of tokens that can be identified
    in a regular expression. These tokens are used to classify and process
    parts of the input string during tokenization.

    Attributes:
        LITERAL: Represents literal characters (e.g., "a", "b", "1").
        ESCAPE_SEQUENCE: Represents escape sequences (e.g., \\n, \\t).
        CHARACTER_CLASS: Represents character classes (e.g., [a-z], \d).
        CAPTURE_GROUP: Represents capture groups (e.g., (abc)).
        QUANTIFIER: Represents quantifiers (e.g., {1,3}, +, *).
        DOT: Represents the dot symbol (.) which matches any character.
        SPECIAL: Represents special symbols (e.g., ^, $, |).
    """

    LITERAL = "Literal"
    ESCAPE_SEQUENCE = "Escape Sequence"
    CHARACTER_CLASS = "Character Class"
    CAPTURE_GROUP = "Capture Group"
    QUANTIFIER = "Quantifier"
    DOT = "Dot"
    SPECIAL = "Special Symbol"
    OTHER = "Other"


# RegexTokenizer class for tokenizing and validating regular expressions
class RegexTokenizer:
    """
    A regex tokenizer for tokenizing and validating regular expressions.
    This class processes an input string and divides it into tokens based
    on the rules of regular expressions. It handles escape sequences,
    character classes, quantifiers, capture groups, and other components.

    Attributes:
        input_string: The input regular expression string to be tokenized.
        tokens: A list of tokens identified in the input string.
        token_types: A list of token types corresponding to the tokens.
        literals: Characters that are treated as literals by default.
        special_symbols: Symbols with special meanings in regular expressions.
        unconditional_characters: Characters that are always valid.
        quantifier_allowed_preceding_token_types: Token types that can precede quantifiers.

    Methods:
        __tokenize: Divides the input string into tokens.
        __handle_escape_sequence: Processes escape sequences in the input.
        __handle_square_brackets: Processes character classes (e.g., [a-z]).
        __handle_curly_brackets: Processes quantifiers (e.g., {1,3}).
        __handle_capture_group: Processes capture groups (e.g., (abc)).
    """

    def __init__(self, input_string: str):
        """
        Initialize the RegexTokenizer with the input string and set up attributes.

        Args:
            input_string (str): The regular expression string to be tokenized.
        """
        # Initialize attributes for processing the input string
        self.__input_string = input_string
        self.i = 0
        self.symbol: str = None
        self.tokens = []
        self.token_types = []
        self.input_string_length = len(input_string)
        self.literals = string.ascii_letters + "." + string.digits
        self.special_symbols = "$^+*?|"
        self.unconditional_characters = self.literals + self.special_symbols
        self.input_iterable = iter(enumerate(self.input_string))  # Iterable for processing input
        self.quantifier_allowed_preceding_token_types = [
            TokenTypes.LITERAL,
            TokenTypes.CHARACTER_CLASS,
            TokenTypes.CAPTURE_GROUP,
            TokenTypes.DOT,
            TokenTypes.ESCAPE_SEQUENCE,
        ]
        self.__tokenize()  # Tokenize the input string.

    @property
    def input_string(self) -> str:
        """
        Getter for the input string.

        Returns:
            str: The input regular expression string.
        """
        return self.__input_string

    def __tokenize(self):
        """
        Tokenize the input string into components of the regular expression.

        Raises:
            NotImplementedError: If an unrecognized symbol is encountered.
            RegexTokenizerError: If tokenization rules are violated.
        """
        while True:
            try:
                # Process each character in the input string
                self.i, self.symbol = next(self.input_iterable)

                match self.symbol:
                    case "\\":
                        # Handle escape sequences
                        self.tokens.append(self.__handle_escape_sequence())
                        self.token_types.append(TokenTypes.ESCAPE_SEQUENCE)

                    case "[":
                        # Handle character classes
                        self.tokens.append(self.__handle_square_brackets())
                        self.token_types.append(TokenTypes.CHARACTER_CLASS)

                    case "{":
                        # Handle quantifiers
                        try:
                            previous = self.token_types[-1]
                        except IndexError as exc:
                            raise RegexTokenizerError(
                                "Quantifier braces must be preceded, by a valid token."
                            ) from exc

                        if previous not in self.quantifier_allowed_preceding_token_types:
                            raise RegexTokenizerError(
                                "Quantifier braces must be preceded, by a valid token."
                            )
                        self.tokens.append(self.__handle_curly_brackets())
                        self.token_types.append(TokenTypes.QUANTIFIER)

                    case "(":
                        # Handle capture groups
                        self.tokens.append(self.__handle_capture_group())
                        self.token_types.append(TokenTypes.CAPTURE_GROUP)

                    case _ if self.symbol in self.literals:
                        # Handle literal characters
                        self.tokens.append(self.symbol)
                        self.token_types.append(TokenTypes.LITERAL)

                    case _ if self.symbol in self.special_symbols:
                        # Handle special symbols
                        self.tokens.append(self.symbol)
                        self.token_types.append(TokenTypes.SPECIAL)

                    case _:
                        # Handle other characters
                        self.tokens.append(self.symbol)
                        self.token_types.append(TokenTypes.OTHER)

            except StopIteration:
                # End of input string
                break

    def __progress_iterable(self, amount: int) -> None:
        """
        Advance the input iterable by a specified amount.

        Args:
            amount (int): The number of steps to skip in the input iterable.
        """
        self.input_iterable = islice(self.input_iterable, amount, None)
        self.i += amount

    def __handle_escape_sequence(self) -> str:
        """
        Handle escape sequences in the input string.

        Returns:
            str: The processed escape sequence token.

        Raises:
            RegexTokenizerError: If the escape sequence is invalid.
            EscapeSequenceLengthError: If the escape sequence is incomplete.
            EndsWithBackslashError: If the input ends with a backslash.
            EscapeSequenceEndError: If the escape sequence ends unexpectedly.
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
                    for char in self.input_string[self.i + 2 : self.i + escape_sequence_length]
                ):
                    print(f"{self.input_string[self.i : -1]}")
                    raise RegexTokenizerError(
                        f'Invalid escape sequence "{self.input_string[self.i : self.i + escape_sequence_length]}" '
                        f"at index {self.i}. Expected hexadecimal characters."
                    )

            # build the token
            token = self.input_string[self.i : self.i + escape_sequence_length]

            # Validate the length of the escape sequence
            if len(token) < escape_sequence_length:
                raise EscapeSequenceLengthError(
                    f'Incomplete escape sequence "\\{escape_type}" at index {self.i}. '
                    f"Expected length: {escape_sequence_length}, but got {len(token)}. "
                    f"Input: {self.input_string}\n"
                    f"{' ' * (7 + self.i)}{'^' * len(token)}"
                )

            self.__progress_iterable(escape_sequence_length - 1)

            return token

        except IndexError as exc:
            raise EndsWithBackslashError('input string cannot end in a backslash "\\"') from exc

    def __handle_square_brackets(self) -> str:
        """
        Handle character classes enclosed in square brackets.

        Returns:
            str: The processed character class token.

        Raises:
            RegexTokenizerError: If invalid character class rules are violated.
            UnclosedGroupError: If the character class is not properly closed.
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
                                raise RegexTokenizerError(
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
                                        raise RegexTokenizerError(
                                            f"Invalid range: '{token[-1]}-{next_symbol}' uses a range character with an already used range."
                                        )
                                    nonindependent_character_indices.extend([self.i - 2, self.i])
                                    token += symbol
                                    token += next_symbol
                                else:
                                    raise RegexTokenizerError(
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

        return token

    def __handle_curly_brackets(self):
        """
        Handle quantifiers enclosed in curly brackets.

        Returns:
            str: The processed quantifier token.

        Raises:
            RegexTokenizerError: If invalid quantifier rules are violated.
            UnclosedGroupError: If the quantifier is not properly closed.
        """
        token = self.symbol  # Start building the token with the opening curly brace
        comma_used = False  # Track if a comma has been used in the quantifier
        previous_number = None  # Store the previous number for range validation

        while True:
            try:
                self.i, symbol = next(self.input_iterable)  # Get the next character

                match symbol:

                    case "}":
                        # Closing curly brace indicates the end of the quantifier
                        if len(token) == 1:
                            raise RegexTokenizerError(
                                "Quantifier braces cannot be empty! Ensure the format is {n}, {n,}, or {n,m}."
                            )
                        token += symbol
                        break

                    case ",":
                        # Handle the comma in quantifiers (e.g., {n,} or {n,m})
                        if comma_used:
                            raise RegexTokenizerError(
                                "Quantifier braces cannot include multiple commas!"
                            )
                        if previous_number is None:
                            raise RegexTokenizerError(
                                "Quantifier braces cannot start with a comma! Ensure the format is {n} or {n,m}."
                            )
                        comma_used = True
                        token += symbol

                    case _ if symbol in string.digits:
                        # Handle digits in the quantifier
                        number = self.__get_number(symbol)  # Extract the full number
                        if comma_used:
                            # Ensure the range is increasing (e.g., {n,m} where n < m)
                            if previous_number and previous_number >= number:
                                raise RegexTokenizerError(
                                    "Range specified in quantifier braces must be rising!"
                                )
                        token += str(number)
                        previous_number = number

                    case _:
                        # Raise an error for invalid characters in the quantifier
                        raise RegexTokenizerError(
                            f'Invalid symbol "{symbol}" in quantifier braces. Only digits and a comma are allowed.'
                        )

            except StopIteration as exc:
                # Raise an error if the quantifier is not properly closed
                raise UnclosedGroupError("Quantifier braces were not closed!") from exc

        return token

    def __get_number(self, initial_digit: str) -> int:
        """
        Extract a number from the input string within quantifier braces.

        Args:
            initial_digit (str): The first digit of the number.

        Returns:
            int: The complete number parsed from the input.

        Raises:
            UnclosedGroupError: If the quantifier braces are not properly closed.
            RegexTokenizerError: If an invalid symbol is encountered in the braces.
        """
        digits = [initial_digit]  # Start building the number with the initial digit
        i = self.i  # Track the current index

        while i + 1 < self.input_string_length:
            i += 1
            symbol = self.input_string[i]  # Get the next character

            if symbol in ",}":
                # Stop parsing if a comma or closing brace is encountered
                break

            if symbol not in string.digits:
                # Raise an error for invalid characters in the number
                raise RegexTokenizerError(
                    f'Invalid symbol "{symbol}" in quantifier braces. Only digits and a comma are allowed.'
                )

            self.i, _ = next(self.input_iterable)  # Advance the iterator
            digits.append(symbol)  # Add the digit to the list

        else:
            # Raise an error if the quantifier braces are not properly closed
            raise UnclosedGroupError("Quantifier braces were not closed!")

        return int("".join(digits))  # Convert the list of digits to an integer

    def __handle_capture_group(self):
        """
        Handle capture groups enclosed in parentheses.

        Returns:
            str: The processed capture group token.

        Raises:
            UnclosedGroupError: If the capture group is not properly closed.
            NotImplementedError: If an unexpected error occurs.
        """
        token = self.symbol  # Start building the token with the opening parenthesis

        i = 0  # Track the position within the capture group
        while True:
            try:
                self.i, symbol = next(self.input_iterable)  # Get the next character
                i += 1

                match symbol:

                    case "\\":
                        # Handle escape sequences within the capture group
                        token += self.__handle_escape_sequence()

                    case "(":
                        # Handle nested capture groups
                        token += self.__handle_capture_group()

                    case ")":
                        # Closing parenthesis indicates the end of the capture group
                        token += symbol
                        break

                    case _:
                        # Add other characters to the token
                        token += symbol

            except StopIteration as exc:
                # Raise an error if the capture group is not properly closed
                raise UnclosedGroupError("Capture Group was not closed!") from exc

        return token


if __name__ == "__main__":
    pass
