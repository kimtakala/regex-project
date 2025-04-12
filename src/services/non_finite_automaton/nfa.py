from services import shunting_yard as shunt
from typing import List


class State:
    def __init__(self, label=None):
        self.label = label  # Character label, None for epsilon
        self.edge1 = None  # First transition
        self.edge2 = None  # Second transition


class NondeterministicFiniteAutomaton:
    def __init__(self, initial_state=None, accept_state=None):
        self.initial_state = initial_state
        self.accept_state = accept_state


# Alias for NondeterministicFiniteAutomaton
nfa = NondeterministicFiniteAutomaton


def follow_es(initial_state) -> set[State]:
    """
    Follow epsilon transitions
    """
    states = set()
    stack = [initial_state]

    while stack:
        state = stack.pop()
        if state not in states:
            states.add(state)
            if state.label is None:  # Epsilon transition
                if state.edge1 is not None:
                    stack.append(state.edge1)
                if state.edge2 is not None:
                    stack.append(state.edge2)
    return states


def compileRegex(postfix):
    nfa_stack: List[nfa] = []

    for character in postfix:
        match character:

            case "*":

                nfa1 = nfa_stack.pop()
                initial_state = State()
                accept_state = State()
                initial_state.edge1 = nfa1.initial_state
                initial_state.edge2 = accept_state
                nfa1.accept_state.edge1 = nfa1.initial_state
                nfa1.accept_state.edge2 = accept_state
                nfa_stack.append(nfa(initial_state, accept_state))

            case ".":

                nfa2 = nfa_stack.pop()
                nfa1 = nfa_stack.pop()
                nfa1.accept_state.edge1 = nfa2.initial_state
                nfa_stack.append(nfa(nfa1.initial_state, nfa2.accept_state))

            case "|":

                nfa2 = nfa_stack.pop()
                nfa1 = nfa_stack.pop()
                initial_state = State()
                accept_state = State()
                initial_state.edge1 = nfa1.initial_state
                initial_state.edge2 = nfa2.initial_state
                nfa1.accept_state.edge1 = accept_state
                nfa2.accept_state.edge1 = accept_state
                nfa_stack.append(nfa(initial_state, accept_state))

            case "+":

                nfa1 = nfa_stack.pop()
                initial_state = State()
                accept_state = State()
                initial_state.edge1 = nfa1.initial_state
                nfa1.accept_state.edge1 = nfa1.initial_state
                nfa1.accept_state.edge2 = accept_state
                nfa_stack.append(nfa(initial_state, accept_state))

            case "?":

                nfa1 = nfa_stack.pop()
                initial_state = State()
                accept_state = State()
                initial_state.edge1 = nfa1.initial_state
                initial_state.edge2 = accept_state
                nfa1.accept_state.edge1 = accept_state
                nfa_stack.append(nfa(initial_state, accept_state))

            case _:

                # Literal character
                initial_state = State(character)
                accept_state = State()
                initial_state.edge1 = accept_state
                nfa_stack.append(nfa(initial_state, accept_state))

    return nfa_stack.pop()


def matchRegex(infix, string):
    postfix = shunt(infix)
    # Uncomment the next line to see the postfix expression
    # print("Postfix:", postfix)

    nfa = compileRegex(postfix)

    current_states = set(follow_es(nfa.initial_state))
    future_states = set()

    for character in string:
        for state in current_states:
            if state.label == character:
                next_states = follow_es(state.edge1)
                future_states.update(next_states)
        current_states = future_states
        future_states = set()

    return nfa.accept_state in current_states


def main():
    infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c"]
    strings = ["", "abc", "abbc", "abcc", "abad", "abbbc"]

    for infix in infixes:
        for string in strings:
            if not string:
                string = '""'
            result = matchRegex(infix, string)
            print(("True " if result else "False ") + infix + " " + string)
        print()


if __name__ == "__main__":
    main()
