from parser import Parser

if __name__ == "__main__":
    print("Regex: ", end="")
    regex = input()
    predicate = Parser(regex).as_predicate()

    print("Input: ", end="")
    while (sequence := input()) != "":
        print(f"Matches: {predicate(sequence)}")
        print("Input: ", end="")