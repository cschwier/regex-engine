import unittest

from regex import Parser


class StarTest(unittest.TestCase):
    def setUp(self) -> None:
        self.testee = Parser("b*bd").as_predicate()

    def test_abc_acceptance(self):
        assert self.testee("bbbd")

class PlusTest(unittest.TestCase):
    def setUp(self) -> None:
        self.testee = ...

class QuestionMarkTest(unittest.TestCase):
    def setUp(self) -> None:
        self.testee = ...

class ExactlyEnTimesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.testee = ...

class EnOrMoreTimesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.testee = ...

class EnToEmTimesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.testee = Parser("ab{2,3}b{2,3}").as_predicate()

    def test_too_little(self):
        assert not self.testee("abbb")

    def test_min(self):
        assert self.testee("abbbb")

    def test_max(self):
        assert self.testee("abbbbbb")

    def test_too_many(self):
        assert not  self.testee("abbbbbbb")

