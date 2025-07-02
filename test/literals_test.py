import unittest

from src.regex import Parser

class RegexWildcardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.testee = Parser("abc").as_predicate()

    def test_abc_acceptance(self):
        assert self.testee("abc")

    def test_abc_prefix_rejection(self):
        assert not  self.testee("xabc")

    def test_abc_suffix_rejection(self):
        assert not  self.testee("abcx")
