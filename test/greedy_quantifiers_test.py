import unittest

from regex import Parser


class StarTest(unittest.TestCase):
    def setUp(self) -> None:
        self.testee = Parser("bb*bd").as_predicate()

    def test_abc_acceptance_many(self):
        assert self.testee("bbbbbbbbbd")

    def test_abc_acceptance_some(self):
        assert self.testee("bbbd")

    def test_abc_acceptance_min(self):
        assert self.testee("bbd")

    def test_abc_rejection(self):
        assert not self.testee("bd")

class PlusTest(unittest.TestCase):
    def setUp(self) -> None:
        self.testee = Parser("bb+b+bd").as_predicate()

    def test_abc_acceptance_min(self):
        assert self.testee("bbbbd")

    def test_abc_acceptance_some(self):
        assert self.testee("bbbbbbd")

    def test_abc_acceptance_many(self):
        assert self.testee("bbbbbbbbbbbbd")

    def test_abc_rejection_1(self):
        assert self.testee("bbbd")

    def test_abc_rejection_2(self):
        assert self.testee("bbbd")

    def test_abc_rejection_3(self):
        assert self.testee("bbd")

    def test_abc_rejection_4(self):
        assert self.testee("bd")

    def test_abc_rejection_5(self):
        assert self.testee("d")

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
        self.testee = Parser("ab{2,3}b{3,4}c").as_predicate()

    def test_too_little(self):
        assert not self.testee("abbbbc")

    def test_min(self):
        assert self.testee("abbbbbc")

    def test_max(self):
        assert self.testee("abbbbbbbc")

    def test_too_many(self):
        assert not self.testee("abbbbbbbbc")

class EmptyRemainingStringOnBacktracking(unittest.TestCase):
    def setUp(self) -> None:
        self.testee = Parser("ab{1,2}b{1,2}").as_predicate()

    def test_back_track_on_empty_remaining_sequence(self):
        assert self.testee("abb")
