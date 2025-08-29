import unittest

from regex import Parser

class PathologicalRegexTest(unittest.TestCase):

    def test_reverse_range(self):
        parser_constructor = lambda: Parser("[c-a]")
        self.assertRaises(BaseException, parser_constructor)