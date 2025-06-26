# regex-engine
Minimal Chomksy-3 parser and evaluator toy-project

## Planned features in order of implementation:

1. Exact words of trivial literals:\
   Example Regex: `abc`\
   Example Matches: `abc`
2. Wildcard:\
   Example Regex: `a.c`\
   Example Matches: `abc`, `aöc`
3. (literal) Character Class:\
   Example Regex: `a[bcd]e`\
   Example Matches: `abe`, `ace`, `ade`
4. Character Group Class:\
   Example Regex: `a[b-d]e`\
   Example Matches: `abe`, `ace`, `ade`
5. Character Class Negations:\
   Example Regex: `a[^b-d]e`\
   Example Matches: `axe`
6. Symbol Repetitions:\
   Example Regex: `ab+` / `ab*`\
   Example Matches: `ab`, `abb` / `a`, `ab`
7. Escaping:\
   Example Regex: `a\[b\+`\
   Example Matches: `a[b+`
8. t.b.c
