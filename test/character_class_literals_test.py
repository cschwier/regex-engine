import unittest

from src.regex import Parser


class RegexWildcardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.testee = Parser("a[xy.]c").as_predicate()

    def test_literal1_acceptance(self):
        self.assertTrue(self.testee("axc"))

    def test_literal2_acceptance(self):
        self.assertTrue(self.testee("ayc"))

    def test_literal_dot_acceptance(self):
        self.assertTrue(self.testee("a.c"))

    def test_literal_rejection(self):
        self.assertFalse(self.testee("abc"))

    def test_multiple_correct_literals_rejection(self):
        self.assertFalse(self.testee("axyc"))
