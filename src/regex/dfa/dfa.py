from typing import Callable, Optional, Annotated, Literal, Any
from abc import ABC, abstractmethod
from sys import maxsize

from regex.utils import CharacterRange

in_backtracking: Annotated[bool, "Global tracker whether current state is in backtracking"] = False

class Matcher(ABC, Callable[[str], tuple[Optional[int], str]]):
    next_state: int

    @abstractmethod
    def __call__(self, remaining_text: str) -> tuple[Optional[int], str]:
        pass

    def reset(self):
        pass

    def has_next(self) -> bool:
        return False


class LiteralMatcher(Matcher):
    def __init__(self, literal: str, next_state: int):
        self.literal = literal
        self.next_state = next_state

    def __call__(self, remaining_text: str):
        if remaining_text[0] == self.literal:
            return self.next_state, remaining_text[1:]
        return None, remaining_text

class WildcardMatcher(Matcher):
    def __init__(self, next_state: int):
        self.next_state = next_state

    def __call__(self, remaining_text: str):
        return self.next_state, remaining_text[1:]

class CharacterClassMatcher(Matcher):
    def __init__(self, character_class: list[CharacterRange], is_negation: bool, target_state: int):
        self.character_class = character_class
        self.is_negation = is_negation
        self.next_state = target_state

    def __call__(self, remaining_text: str):
        predicate: Callable[[CharacterRange], bool] = lambda char_range: (char_range.start <= ord(remaining_text[0]) <= char_range.end)

        # != is XOR since both are bool
        # Either negation + not any OR not negated + any
        return (self.next_state, remaining_text[1:]) if self.is_negation != any(predicate(cr) for cr in self.character_class) else (None, remaining_text)

class GreedyQuantifierMatcher(Matcher):
    remaining_matcher_text: Optional[str]
    iteration_limit: Optional[int]

    def __init__(self, matcher: Matcher, min_repetitions: int, max_repetitions: Optional[int], target_state: int):
        self.matcher = matcher
        self.next_state = target_state

        self.min_repetitions = min_repetitions
        self.max_repetitions: int = max_repetitions if max_repetitions else maxsize

        self.reset()

    def has_next(self) -> bool:
        return (
            self.last_check_succeeded
                and (
                    not self.iteration_limit
                    or  self.iteration_limit >= self.min_repetitions
                )
        )

    def reset(self):
        # TODO
        self.remaining_matcher_text = None
        self.iteration_limit = self.max_repetitions

    def __call__(self, remaining_text: str):
        # pattern: [ab]{2,3}b
        # string: ababb

        i = 0

        while i < self.iteration_limit and remaining_text:
            potential_next_state, potential_remaining_text = self.matcher(remaining_text)

            if not potential_next_state:
                break

            remaining_text = potential_remaining_text
            i += 1

        # TODO: Check limit
        if i >= self.min_repetitions:
            self.last_check_succeeded = True
            self.iteration_limit -= 1
            return self.next_state, remaining_text
        else:
            self.last_check_succeeded = False
            return None, remaining_text


class Dfa:
    def __init__(self, end_states: list[int], transitions: dict[int, Callable[[str], int]]) -> None:
        self.transitions = transitions
        self.end_states = end_states



    def check(self, text: str):
        current_state = 0

        remaining_text = text
        handled_matchers: list[tuple[Callable, int]] = []

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

            handled_matchers.append((next_matcher, remaining_text))
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
