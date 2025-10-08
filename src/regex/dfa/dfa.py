from typing import Callable, Optional, Annotated, Literal, Any
from abc import ABC, abstractmethod

from regex.utils import CharacterRange

in_backtracking: Annotated[bool, "Global tracker whether current state is in backtracking"] = False

class Matcher(ABC):
    next_state: int

    @abstractmethod
    def __call__(self, remaining_text: str) -> tuple[Optional[int], str]:
        pass

    def reset(self):
        pass

    def has_next(self) -> bool:
        return False


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
        self.next_state = target_state
        self.last_try = None

    def _next_option(self, remaining_text: str):
        # TODO
        pass

    def has_next(self) -> bool:
        # TODO
        pass

    def reset(self):
        # TODO
        pass


    def __call__(self, remaining_text: str):
        match self.remaining_text:
            case None:
                # Not executed yet
                self._build_greediest_option(remaining_text)
            case "":
                # No more options available
                return None, remaining_text

        return self.next_state, self._next_option()


    def _build_greediest_option(self, input_text: str) -> None:
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
        current_state = 0

        remaining_text = text
        handled_matchers = []

        while remaining_text:   # bbbbbc -> c
            # regex: ab*bc
            # input: abbbbbc

            # a -True-> bbbbb -True-> b -False->  bbbb -True-> b -True-> c -True-> ✅

            next_matcher = self.transitions.get(current_state)

            # TODO: Changeme
            if next_matcher is None:
                next_matcher, remaining_text = self._backtrack(handled_matchers)
                # No more options left in handled matchers --> RegEx fails
                if not next_matcher:
                    return False

            handled_matchers.insert(0, (next_matcher, remaining_text))
            current_state, remaining_text = next_matcher(remaining_text)

        return current_state in [self.end_states]

    def _backtrack(self, handled_matchers: list[tuple[Matcher, str]]) -> tuple[Optional[Matcher], Optional[str]]:
        while handled_matchers:
            matcher, remaining_text = handled_matchers.pop()
            if matcher.has_next():
                return matcher, remaining_text
            else:
                matcher.reset()

        return None, None
