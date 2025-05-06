"""
This is a module for converting text
into postfix notation with the shunting yard algorithm.
"""

from .exceptions import MismatchedParenthesesError, PostfixError


def shunting_yard(infix):
    """
    Shunting yard algorithm for regex
    """
    # Handle empty regex
    if not infix:
        return ""

    specials = {"*": 60, "+": 55, "?": 50, ".": 40, "|": 20}
    postfix = ""
    stack = []

    for character in infix:
        if character == "(":
            stack.append(character)
        elif character == ")":
            while stack and stack[-1] != "(":
                postfix += stack.pop()
            if stack and stack[-1] == "(":
                stack.pop()  # Remove '('
            else:
                raise MismatchedParenthesesError("Mismatched parentheses: ')' without matching '('")
        elif character in specials:
            while (
                stack
                and stack[-1] in specials
                and (
                    specials[character] < specials[stack[-1]]
                    or (specials[character] == specials[stack[-1]] and character in ".*")
                )
            ):
                postfix += stack.pop()
            stack.append(character)
        elif character.isalnum():
            postfix += character
        else:
            raise PostfixError(f"Invalid character in regex: {character}")

    while stack:
        if stack[-1] == "(":
            raise MismatchedParenthesesError("Mismatched parentheses: '(' without matching ')'")
        postfix += stack.pop()

    return postfix
