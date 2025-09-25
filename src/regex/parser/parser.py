from typing import Callable, Any, Optional

from regex.dfa import Dfa
from regex.dfa.dfa import LiteralMatcher, WildcardMatcher, CharacterClassMatcher, GreedyQuantifierMatcher
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

def parse_explicit_greedy_quantifier(greedy_quantifier: str,) -> tuple[int, int]:
    vals = greedy_quantifier.split(",")
    assert len(vals) == 2, f"Provided more than one comma in greedy quantifier {greedy_quantifier}"
    min_repetitions, max_repetitions = vals
    try:
        return int(min_repetitions), int(max_repetitions)
    except ValueError:
        raise AssertionError(f"Provided non-integer arguments in greedy quantifier {greedy_quantifier}")


# Frage Christian: Sollte die Funktion Teil der Klasse sein? Wieso (nicht)?
def iterate_pattern_until_character(pattern: str, break_character: str, start_index: int) -> tuple[str, int]:
    _i = start_index + 1
    character_group = ""
    while _i < len(pattern):
        character = pattern[_i]
        if character == break_character:
            break
        character_group += character
        _i += 1
    return character_group, _i


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
                    character_group, i = iterate_pattern_until_character(self.pattern, break_character="]", start_index=i)
                    numeric_character_group, is_negation = parse_character_group(character_group)
                    transitions[i] = CharacterClassMatcher(numeric_character_group, is_negation, i+1)
                case "*" | "+" | "?" | "{":
                    # Cases where previous matcher must be iterated upon. Since keys for transitions are monotonically
                    # increasing, so the previous transition is the one with the highest key
                    try:
                        last_transition = transitions.pop(max(transitions, key=transitions.get))
                    except ValueError | KeyError:
                        raise AssertionError("Specified Greedy Quantifier but no previous transition available")
                    match character:
                        case "*":
                            transitions[i] = GreedyQuantifierMatcher(last_transition, min_repetitions=0, max_repetitions=len(self.pattern[i:]), target_state=i+1)
                        case "+":
                            transitions[i] = GreedyQuantifierMatcher(last_transition, min_repetitions=1, max_repetitions=len(self.pattern[i:]), target_state=i+1)
                        case "?":
                            transitions[i] = GreedyQuantifierMatcher(last_transition, min_repetitions=0, max_repetitions=1, target_state=i+1)
                        case "{":
                            greedy_quantifier, i = iterate_pattern_until_character(self.pattern, break_character="}", start_index=i)
                            min_repetitions, max_repetitions = parse_explicit_greedy_quantifier(greedy_quantifier)
                            transitions[i] = GreedyQuantifierMatcher(last_transition, min_repetitions=min_repetitions, max_repetitions=max_repetitions, target_state=i+1)
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
