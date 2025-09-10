from typing import Callable, Any

from regex.dfa import Dfa
from regex.dfa.dfa import LiteralMatcher, WildcardMatcher, CharacterClassMatcher
from regex.utils import CharacterRange

def parse_character_group(character_group: str) -> tuple[list[CharacterRange], bool]:
    stack = []

    character_group_iterator = iter(character_group)
    is_negotiation = character_group[0] == "^"
    if is_negotiation:
        next(character_group_iterator)

    while c := next(character_group_iterator, None):
        match c:
            case "-":
                old = stack.pop()
                stack.append(CharacterRange(old.start, ord(next(character_group_iterator))))
            case _:
                stack.append(CharacterRange(ord(c), ord(c)))

    return stack, is_negotiation

class Parser:

    def __init__(self, pattern: str):
        self.pattern = pattern
        self._dfa = self._parse()

    def _parse(self) -> Dfa:
        transitions = {}

        i = 0
        while i < len(self.pattern):
            character = self.pattern[i]
            matcher_state_index = i
            match character:
                case "[":
                    i += 1
                    character_group = ""
                    while i < len(self.pattern):
                        character = self.pattern[i]
                        if character == "]":
                            break
                        character_group += character
                        i += 1
                    numeric_character_group, is_negation = parse_character_group(character_group)
                    transitions[matcher_state_index] = CharacterClassMatcher(numeric_character_group, is_negation, i+1)
                case ".":
                    transitions[matcher_state_index] = WildcardMatcher(i+1)
                case _:
                    transitions[matcher_state_index] = LiteralMatcher(character, i+1)
            i += 1

        acceptance_states = list(transitions.values())[-1].next_state
        return Dfa(acceptance_states, transitions)


    def as_predicate(self) -> Callable[[str], bool]:
        predicate = lambda inp : self._dfa.check(inp)
        return predicate
