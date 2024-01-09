import unittest
from random import randint
from typing import Any

from txtdata import TxtData


def _random_sample(n: int = 1_000) -> list[dict[str, Any]]:
    return [
        {
            'A': randint(0, 100),
            'B': randint(0, 10),
            'C': randint(0, 1_000),
        }
        for _ in range(n)
    ]


class TestTxtData(unittest.TestCase):
    def test_creation_empty(self):
        txt = TxtData()
        assert txt.empty

    def test_len(self):
        data = _random_sample(50)
        txt = TxtData(data)
        assert len(txt) == 50

    def test_fields(self):
        data = _random_sample(50)
        txt = TxtData(data)
        assert txt.fields == ['A', 'B', 'C']

    def test_insert_dict(self):
        txt = TxtData()
        txt.insert({'A': 123})
        txt.insert({'B': 111})
        txt.insert({'A': 182, 'C': 'das'})
        assert txt.data == [
            {'A': 123, 'B': None, 'C': None},
            {'A': None, 'B': 111, 'C': None},
            {'A': 182, 'B': None, 'C': 'das'},
        ]

    def test_insert_keyword(self):
        txt = TxtData()
        txt.insert(A=123, C=123)
        txt.insert(B=111)
        txt.insert(A=182, C='das')
        assert txt.data == [
            {'A': 123, 'B': None, 'C': 123},
            {'A': None, 'B': 111, 'C': None},
            {'A': 182, 'B': None, 'C': 'das'},
        ]

    def test_filter(self):
        data = [
            {'A': 10, 'B': 50, 'C': 'asd'},
            {'A': None, 'B': 10, 'C': 50},
            {'A': 150, 'B': 50, 'C': 39},
            {'A': 123, 'B': 33, 'C': 12},
            {'A': 55, 'B': None, 'C': 44},
            {'A': 32, 'B': 50, 'C': 2},
        ]
        txt = TxtData(data)
        filtered_txt = txt.filter(B=50)
        assert len(filtered_txt) == 3
