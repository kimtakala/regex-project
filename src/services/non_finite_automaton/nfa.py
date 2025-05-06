"""
This file set's up a non-deterministic finite automaton and uses it to compile regex.
"""

from typing import List, Set
from src.services.postfix.postfix import shunting_yard as shunt
from .exceptions import InvalidRegexError, EmptyRegexError


class State:
    """
    This is a class for the state of an nfa.
    """

    def __init__(self, label=None):
        self.label = label  # Character label, None for epsilon
        self.edge1 = None  # First transition
        self.edge2 = None  # Second transition


class NondeterministicFiniteAutomaton:
    """
    this is a nfa class, for processing regex.
    """

    def __init__(self, initial_state=None, accept_state=None):
        self.initial_state = initial_state
        self.accept_state = accept_state


# Alias for NondeterministicFiniteAutomaton
NFA = NondeterministicFiniteAutomaton


def follow_es(initial_state) -> Set[State]:
    """
    Follow epsilon transitions from a state and return all reachable states
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


def compile_regex(postfix):
    """
    Compile a postfix regex expression into an NFA.
    """
    nfa_stack: List[NFA] = []

    # Handle empty regex
    if not postfix:
        raise EmptyRegexError("The provided regex is empty.")

    for character in postfix:
        match character:

            case "*":
                if not nfa_stack:
                    raise InvalidRegexError("Invalid regex: * operator with no operand")

                nfa1 = nfa_stack.pop()
                initial_state = State()
                accept_state = State()
                initial_state.edge1 = nfa1.initial_state
                initial_state.edge2 = accept_state
                nfa1.accept_state.edge1 = nfa1.initial_state
                nfa1.accept_state.edge2 = accept_state
                nfa_stack.append(NFA(initial_state, accept_state))

            case ".":
                if len(nfa_stack) < 2:
                    raise InvalidRegexError("Invalid regex: . operator requires two operands")

                nfa2 = nfa_stack.pop()
                nfa1 = nfa_stack.pop()
                nfa1.accept_state.edge1 = nfa2.initial_state
                nfa_stack.append(NFA(nfa1.initial_state, nfa2.accept_state))

            case "|":
                if len(nfa_stack) < 2:
                    raise InvalidRegexError("Invalid regex: | operator requires two operands")

                nfa2 = nfa_stack.pop()
                nfa1 = nfa_stack.pop()
                initial_state = State()
                accept_state = State()
                initial_state.edge1 = nfa1.initial_state
                initial_state.edge2 = nfa2.initial_state
                nfa1.accept_state.edge1 = accept_state
                nfa2.accept_state.edge1 = accept_state
                nfa_stack.append(NFA(initial_state, accept_state))

            case "+":
                if not nfa_stack:
                    raise InvalidRegexError("Invalid regex: + operator with no operand")

                nfa1 = nfa_stack.pop()
                initial_state = State()
                accept_state = State()
                initial_state.edge1 = nfa1.initial_state
                nfa1.accept_state.edge1 = nfa1.initial_state
                nfa1.accept_state.edge2 = accept_state
                nfa_stack.append(NFA(initial_state, accept_state))

            case "?":
                if not nfa_stack:
                    raise InvalidRegexError("Invalid regex: ? operator with no operand")

                nfa1 = nfa_stack.pop()
                initial_state = State()
                accept_state = State()
                initial_state.edge1 = nfa1.initial_state
                initial_state.edge2 = accept_state
                nfa1.accept_state.edge1 = accept_state
                nfa_stack.append(NFA(initial_state, accept_state))

            case "(" | ")":
                raise InvalidRegexError("Parentheses should not appear in postfix notation.")

            case _:
                # Literal character
                initial_state = State(character)
                accept_state = State()
                initial_state.edge1 = accept_state
                nfa_stack.append(NFA(initial_state, accept_state))

    if len(nfa_stack) != 1:
        raise InvalidRegexError(
            f"Invalid regex: too many operands left on stack ({len(nfa_stack)})"
        )

    return nfa_stack.pop()


def match_regex(infix, string):
    """
    Match a string against a regex pattern
    """
    # Convert infix to postfix
    postfix = shunt(infix)

    # Handle empty regex
    if not postfix:
        if string == "":
            return True
        raise EmptyRegexError("The provided regex is empty.")

    # Build the NFA
    nfa_result = compile_regex(postfix)

    # Start with the initial state and follow all epsilon transitions
    current_states = follow_es(nfa_result.initial_state)

    # Process each character in the string
    for c in string:
        next_states = set()

        # For each current state
        for state in current_states:
            # If this state has a matching label
            if state.label == c:
                # Add states reachable through epsilon transitions after consuming the character
                if state.edge1:
                    next_states.update(follow_es(state.edge1))

        # Update current states
        current_states = next_states

        # If we have no valid states, matching fails
        if not current_states:
            return False

    # Check if any current state is an accept state
    return nfa_result.accept_state in current_states
