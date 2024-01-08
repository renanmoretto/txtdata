import unittest

from txtdata import TxtData


class TestTxtData(unittest.TestCase):
    def test_creation_empty(self):
        txt = TxtData()
        assert txt.empty

    def test_insert_dict(self):
        txt = TxtData()
        txt.insert({'A': 123})
        txt.insert({'B': 111})
        txt.insert({'A': 182, 'C': 'das'})
        print(txt.data)
        assert txt.data == [
            {'A': 123, 'B': None, 'C': None},
            {'A': None, 'B': 111, 'C': None},
            {'A': 182, 'B': None, 'C': 'das'},
        ]
