from typing import Callable

from regex.dfa import Dfa
from regex.dfa.dfa import LiteralMatcher, WildcardMatcher, CharacterClassMatcher


class Parser:

    def __init__(self, pattern: str):
        self.pattern = pattern
        self._dfa = self._parse()

    def _parse(self) -> Dfa:
        transitions = {}

        i = 0
        while i < len(self.pattern):
            character = self.pattern[i]
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
                    transitions[i] = CharacterClassMatcher(character_group, i+1)
                case ".":
                    transitions[i] = WildcardMatcher(i+1)
                case _:
                    transitions[i] = LiteralMatcher(character, i+1)
            i += 1

        acceptance_states = list(transitions.values())[-1].next_state
        return Dfa(acceptance_states, transitions)


    def as_predicate(self) -> Callable[[str], bool]:
        predicate = lambda inp : self._dfa.check(inp)
        return predicate
