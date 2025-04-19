from postfix import MismatchedParenthesesError


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
            if not stack or stack[-1] != "(":
                raise MismatchedParenthesesError("Mismatched parentheses: ')' without matching '('")
            stack.pop()  # Remove '('
        elif character in specials:
            while stack and stack[-1] in specials and specials[character] < specials[stack[-1]]:
                postfix += stack.pop()
            stack.append(character)
        else:
            postfix += character

    while stack:
        if stack[-1] == "(":
            raise MismatchedParenthesesError("Mismatched parentheses: '(' without matching ')'")
        postfix += stack.pop()

    return postfix
