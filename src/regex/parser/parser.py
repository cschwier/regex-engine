from typing import Callable

from regex.dfa import Dfa


class Parser:

    def __init__(self, pattern: str):
        self.pattern = pattern
        self._dfa = self._parse()

    def _parse(self) -> Dfa:
        transitions = {}

        for i, char in enumerate(self.pattern):
            transitions[i] = {char: i+1}

        acceptance_states = list(transitions.values())[-1].values()
        return Dfa(acceptance_states, transitions)

    def as_predicate(self) -> Callable[[str], bool]:
        predicate = lambda inp : self._dfa.check(inp)
        return predicate
