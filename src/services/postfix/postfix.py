from services import user_input


def shunting_yard(infix):
    specials = {"*": 60, "+": 55, "?": 50, ".": 40, "|": 20}
    postfix = ""
    stack = []

    for character in infix:
        if character == "(":
            stack.append(character)
        elif character == ")":
            while stack and stack[-1] != "(":
                postfix += stack.pop()
            if stack:
                stack.pop()  # Remove '('
        elif character in specials:
            while stack and stack[-1] in specials and specials[character] <= specials[stack[-1]]:
                postfix += stack.pop()
            stack.append(character)
        else:
            postfix += character

    while stack:
        postfix += stack.pop()

    return postfix


if __name__ == "__main__":
    infix = user_input()

    postfix = shunting_yard(infix)
    print(postfix)
