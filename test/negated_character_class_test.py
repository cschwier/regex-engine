import unittest

from regex import Parser


class NegatedCharacterClassTest(unittest.TestCase):
    def setUp(self) -> None:
        self.testee = Parser("a[^x-z357]c").as_predicate()

    def test_literal_not_in_negated_range1_accepted(self):
        self.assertTrue(self.testee("auc"))

    def test_literal_not_in_negated_range2_accepted(self):
        self.assertTrue(self.testee("aAc"))

    def test_literal_not_in_negated_range3_accepted(self):
        self.assertTrue(self.testee("a2c"))

    def test_literal_not_in_negated_range4_accepted(self):
        self.assertTrue(self.testee("a6c"))

    def test_multiple_correct_literals_rejection(self):
        self.assertFalse(self.testee("au6c"))

    def test_multiple_correct_literals2_rejection(self):
        self.assertFalse(self.testee("aA2c"))

    def test_accept_range_symbol(self):
        """Since the range symbol is not in the negated character class it should be accepted."""
        self.assertFalse(self.testee("a-c"))

    def test_range1_rejection(self):
        self.assertFalse(self.testee("axc"))

    def test_range2_rejection(self):
        self.assertFalse(self.testee("ayc"))

    def test_range3_rejection(self):
        self.assertFalse(self.testee("azc"))

    def test_range4_rejection(self):
        self.assertFalse(self.testee("a3c"))

    def test_range5_rejection(self):
        self.assertFalse(self.testee("a4c"))

    def test_range6_rejection(self):
        self.assertFalse(self.testee("a5c"))
