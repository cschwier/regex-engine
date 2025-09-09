from typing import Callable
from abc import ABC, abstractmethod

from regex.utils import CharacterRange

class Matcher(ABC):
    next_state: int

    @abstractmethod
    def __call__(self, symbol: str) -> int | None:
        pass


class LiteralMatcher(Callable[[str], int], Matcher):
    def __init__(self, literal: str, next_state: int):
        self.literal = literal
        self.next_state = next_state

    def __call__(self, symbol: str) -> int | None:
        if symbol == self.literal:
            return self.next_state
        return None

class WildcardMatcher(Callable[[str], int], Matcher):
    def __init__(self, next_state: int):
        self.next_state = next_state

    def __call__(self, _: str):
        return self.next_state

class CharacterClassMatcher(Callable[[str], int], Matcher):
    def __init__(self, character_class: list[CharacterRange], is_negation: bool, target_state: int):
        self.character_class = character_class
        self.is_negation = is_negation
        self.next_state = target_state

    def __call__(self, symbol: str) -> int | None:
        for i, _range in enumerate(self.character_class):
            is_in_range = _range.start <= ord(symbol) <= _range.end

            match self.is_negation, is_in_range:
                case True, True:
                    return None
                case True, False:
                    if i == len(self.character_class) - 1:
                        return self.next_state
                case False, True:
                    return self.next_state

        return None

class EverythingExceptMatcher(Callable[[str], int], Matcher):
    pass


class Dfa:
    def __init__(self, end_states: list[int], transitions: dict[int, Callable[[str], int]]) -> None:
        self.transitions = transitions
        self.end_states = end_states

    def check(self, text: str):
        current_state = 0

        for symbol in text:
            next_state_callable = self.transitions.get(current_state)

            if next_state_callable is None:
                return False

            current_state = next_state_callable(symbol)

            if current_state is None:
                return False

        return current_state in [self.end_states]

