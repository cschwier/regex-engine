from src.regex.parser import Parser


def test_abc_acceptance():
    checker = Parser("abc").as_predicate()
    assert checker("abc")

def test_abc_rejection():
    checker = Parser("abc").as_predicate()
    assert not checker("abcx")
    assert not checker("xabc")
