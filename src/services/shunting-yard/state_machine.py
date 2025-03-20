"""
Cheat Sheet
Character classes
.	any character except newline
\w \d \s	word, digit, whitespace
\W \D \S	not word, digit, whitespace
[abc]	any of a, b, or c
[^abc]	not a, b, or c
[a-g]	character between a & g
Anchors
^abc$	start / end of the string
\b	word boundary
Escaped characters
\. \* \\	escaped special characters
\t \n \r	tab, linefeed, carriage return
\u00a9	unicode escaped ©
Groups & Lookaround
(abc)	capture group
\1	backreference to group #1
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


class StateMachine:
    def __init__(self, input_string: str):
        self.i = 0
        self.tokens = []
        self.input_string = input_string
        self.input_string_length = len(input_string)
        self.unconditional_characters = "."

    def tokenize(self, input_string):
        input_string = self.input_string

        for i in range(len(input_string)):
            symbol = input_string[i]

            match symbol:

                case "\\":
                    try:
                        self.tokens.append(f"{symbol}{input_string[i+1]}")
                        i += 1
                    except IndexError:
                        raise ValueError('Can\'t end with a backslash character "\\"')

                case _ if symbol in self.unconditional_characters:
                    pass

                case "[":
                    pass

                case "^":
                    if i == 0:
                        pass
                    elif input_string[i - 1] == "[":
                        pass
                    else:
                        self.tokens.append(symbol)

                case "$":
                    if i == (self.input_string_length - 1):
                        pass
                    else:
                        self.tokens.append(symbol)

                case "(":
                    pass

                case "*":
                    pass

                case "+":
                    pass

                case "?":
                    pass

                case "{":
                    pass

                case _:
                    pass


class ParenthesisState:
    def __init__(self, state_machine):
        self.state_machine = state_machine


if __name__ == "__main__":
    pass
