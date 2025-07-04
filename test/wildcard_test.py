import unittest

from regex import Parser


class RegexWildcardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.testee = Parser("a.c").as_predicate()

    def test_literal_acceptance(self):
        self.assertTrue(self.testee("abc"))

    def test_dot_acceptance(self):
        self.assertTrue(self.testee("a.c"))

    def test_question_mark_acceptance(self):
        self.assertTrue(self.testee("a?c"))