import unittest

from utils import extract_title


class TestNodeSplitter(unittest.TestCase):
    def test_extract_h1(self):
        actual = extract_title('# Hello')
        self.assertEqual(actual, 'Hello')

    def test_extract_h1_error(self):
        with self.assertRaises(Exception):
            extract_title('## title')
