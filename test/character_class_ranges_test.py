import unittest

from regex import Parser


class RegexWildcardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.testee = Parser("a[x-z3-5]c").as_predicate()

    def test_range1_acceptance(self):
        self.assertTrue(self.testee("axc"))

    def test_range2_acceptance(self):
        self.assertTrue(self.testee("ayc"))

    def test_range3_acceptance(self):
        self.assertTrue(self.testee("azc"))

    def test_range4_acceptance(self):
        self.assertTrue(self.testee("a3c"))

    def test_range5_acceptance(self):
        self.assertTrue(self.testee("a4c"))

    def test_range6_acceptance(self):
        self.assertTrue(self.testee("a5c"))

    def test_literal_not_in_range_rejection(self):
        self.assertFalse(self.testee("abc"))

    def test_multiple_correct_literals_rejection(self):
        self.assertFalse(self.testee("axyc"))

    def test_multiple_correct_literals2_rejection(self):
        self.assertFalse(self.testee("ay4c"))
