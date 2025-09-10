# regex-engine
Minimal Chomksy-3 parser and evaluator toy-project

## Planned features in order of implementation:

1. [x] Exact words of trivial literals:\
   Example Regex: `abc`\
   Example Matches: `abc`
2. [x] Wildcard:\
   Example Regex: `a.c`\
   Example Matches: `abc`, `aöc`
3. [x] (literal) Character Class:\
   Example Regex: `a[bcd]e`\
   Example Matches: `abe`, `ace`, `ade`
4. [x] Character Class:\
   Example Regex: `a[b-d]e`\
   Example Matches: `abe`, `ace`, `ade`
5. [x] Character Class Negations:\
   Example Regex: `a[^b-d]e`\
   Example Matches: `axe`
6. [ ] Symbol Repetitions:\
   Example Regex: `ab+` / `ab*`, `ab?`\
   Example Matches: `ab`, `abb` / `a`, `abbb` / `a`, `ab`
7. [ ] Escaping:\
   Example Regex: `a\[b\+`\
   Example Matches: `a[b+`
8. t.b.c

## Available Features
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions/Cheatsheet

## Idea

It should be possible to either do this via different classes or functionally (lambdas in Python eval). Let's do both :) 