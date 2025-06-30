from src.regex.dfa import Dfa
from src.regex.parser import Parser

if __name__ == "__main__":
    print("Regex: ", end="")
    regex = input()
    dfa = Parser.parse(regex)

    print("Input: ", end="")
    while (sequence := input()) != "":
        print(f"Matches: {dfa.check(sequence)}")
        print("Input: ", end="")
