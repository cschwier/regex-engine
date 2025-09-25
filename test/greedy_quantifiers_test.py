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
        self.testee = ...
