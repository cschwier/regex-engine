from typing import Callable, Optional, Annotated, Literal
from abc import ABC, abstractmethod

from regex.utils import CharacterRange

in_backtracking: Annotated[bool, "Global tracker whether current state is in backtracking"] = False

class Matcher(ABC):
    next_state: int

    @abstractmethod
    def __call__(self, remaining_text: str) -> tuple[Optional[int], str]:
        pass


class LiteralMatcher(Callable[[str], int], Matcher):
    def __init__(self, literal: str, next_state: int):
        self.literal = literal
        self.next_state = next_state

    def __call__(self, remaining_text: str):
        if remaining_text[0] == self.literal:
            return self.next_state, remaining_text[1:]
        return None, remaining_text

class WildcardMatcher(Callable[[str], int], Matcher):
    def __init__(self, next_state: int):
        self.next_state = next_state

    def __call__(self, remaining_text: str):
        return self.next_state, remaining_text[1:]

class CharacterClassMatcher(Callable[[str], int], Matcher):
    def __init__(self, character_class: list[CharacterRange], is_negation: bool, target_state: int):
        self.character_class = character_class
        self.is_negation = is_negation
        self.next_state = target_state

    def __call__(self, remaining_text: str):
        predicate: Callable[[CharacterRange], bool] = lambda char_range: (char_range.start <= ord(remaining_text[0]) <= char_range.end)

        # != is XOR since both are bool
        # Either negation + not any OR not negated + any
        return (self.next_state, remaining_text[1:]) if self.is_negation != any(predicate(cr) for cr in self.character_class) else (None, remaining_text)

class GreedyQuantifierMatcher(Callable[[str], int], Matcher):
    # TODO: Literal[False] as indication for no max_repetitions seems a bit intransparent
    def __init__(self, matcher: Callable, min_repetitions: int, max_repetitions: int | Literal[False], target_state: int):
        self.matcher = matcher
        self.min_repetitions = min_repetitions
        self.max_repetitions = max_repetitions
        self.next_state = target_state
        self.remaining_text_options = []

    def __call__(self, remaining_text: str):
        global in_backtracking

        if not self.remaining_text_options:
            if in_backtracking:
                # In backtracking, but all options exhausted --> No match
                in_backtracking = False
                return None, remaining_text
            else:
                # Not in backtracking + no Options: First iteration
                self._build_all_options(remaining_text)
                in_backtracking = True

        # Using pop --> Starting from last, most greedy option
        current_option = self.remaining_text_options.pop()
        return self.next_state, current_option

    def _build_all_options(self, input_text: str) -> None:
        """
        Builds all possible remaining_text options

        :param input_text: Input to __call__, i.e., current rest of string
        :return: None
        """
        # |   Pattern   |    Input    |    Potential Remainders    |
        # |-------------|-------------|----------------------------|
        # |    a{2,4}   |    aaaac    | ["aac", "ac", "c"]         |
        # |    b*       |    bbbd     | ["bbbd", "bbd", "bd", "d"] |
        # |    b+       |    bbbd     | ["bbd", "bd", "d"]         |
        # |    c?       |    cdef     | ["cdef", "def"]            |

        # If False at initialization: Can go on as long as possible
        if not self.max_repetitions:
            self.max_repetitions = len(input_text)

        for i in range(self.min_repetitions, self.max_repetitions + 1):
            if i == 0:
                self.remaining_text_options.append(input_text)
                continue

            string_to_match = input_text[0:i]   # up to, but not including i
            remainder = input_text[i:]          # starting from, including i

            if all(next_state for next_state in [self.matcher(s)[0] for s in string_to_match]):
                self.remaining_text_options.append(remainder)


class Dfa:
    def __init__(self, end_states: list[int], transitions: dict[int, Callable[[str], int]]) -> None:
        self.transitions = transitions
        self.end_states = end_states

    def check(self, text: str):
        global in_backtracking

        next_state_callable = None
        current_state = 0
        reset_backtracking = False

        remaining_text = text
        while remaining_text:
            current_state_callable = next_state_callable

            next_state_callable = self.transitions.get(current_state)

            if next_state_callable is None:
                return False

            current_state, remaining_text = next_state_callable(remaining_text)

            if not current_state:
                if in_backtracking:
                    reset_backtracking = True
                    current_state, remaining_text = current_state_callable(remaining_text)
                else:
                    return False
            elif reset_backtracking:
                in_backtracking = False
                reset_backtracking = False

        return current_state in [self.end_states]

