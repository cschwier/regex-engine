from src.regex.dfa import Dfa


class Parser:
    @staticmethod
    def parse(pattern: str) -> Dfa:
        transitions = {}

        for i, char in enumerate(pattern):
            transitions[i] = {char: i+1}

        acceptance_states = list(transitions.values())[-1].values()
        return Dfa(acceptance_states, transitions)
