from src.regex.parser import Parser


def test_abc_true():
    dfa = Parser.parse("abc")

    assert dfa.check("abc")

def test_abc_false():
    dfa = Parser.parse("abc")

    assert not dfa.check("abcc")
