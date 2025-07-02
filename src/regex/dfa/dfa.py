class Dfa:
    def __init__(self, end_states: list[int], transitions: dict[int, dict[str, int]]) -> None:
        self.transitions = transitions
        self.end_states = end_states

    def check(self, inp: str):
        current_state = 0

        for i in inp:
            next_state_lookup = self.transitions.get(current_state)
            if next_state_lookup is None:
                return False

            current_state = next_state_lookup.get(i)
            if current_state is None:
                return False

        return current_state in self.end_states
