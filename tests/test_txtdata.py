import unittest
from random import randint
from typing import Any

from txtdata import TxtData, ShapeError


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

    def test_creation_simple_dict(self):
        txt = TxtData({'A': 123, 'B': 11})
        assert txt.data == [{'A': 123, 'B': 11}]

    def test_creation_list_of_dicts(self):
        list_of_dicts = [
            {'A': 10, 'B': 50, 'C': 'asd'},
            {'A': None, 'B': 10, 'C': 50},
            {'A': 150, 'B': 50, 'C': 39},
            {'A': 123, 'B': 33, 'C': 12},
            {'A': 55, 'B': None, 'C': 44},
            {'A': 32, 'B': 50, 'C': 2},
        ]
        txt = TxtData(list_of_dicts)
        assert txt.data == list_of_dicts

    def test_creation_dict_of_lists(self):
        data = {'A': [1, 2, 3], 'B': ['x', 'y', None]}
        txt = TxtData(data)
        assert txt.data == [
            {'A': 1, 'B': 'x'},
            {'A': 2, 'B': 'y'},
            {'A': 3, 'B': None},
        ]

    def test_creation_dict_of_lists_wrong_shape(self):
        data = {'A': [1, 2, 3], 'B': ['x', 'y']}
        self.assertRaises(ShapeError, TxtData, data)

    def test_eq(self):
        data = {'A': [1, 2, 3], 'B': ['x', 'y', None]}
        txt1 = TxtData(data)
        txt2 = TxtData(data)
        assert txt1 == txt2

    def test_len(self):
        data = _random_sample(50)
        txt = TxtData(data)
        assert len(txt) == 50

    def test_add(self):
        txt1 = TxtData([{'A': 123, 'B': 111}])
        txt2 = TxtData([{'A': 182, 'C': 'das'}])
        txt = txt1 + txt2
        assert txt.data == [
            {'A': 123, 'B': 111, 'C': None},
            {'A': 182, 'B': None, 'C': 'das'},
        ]

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

    def test_insert_list_dicts(self):
        txt = TxtData()
        txt.insert([{'A': 123}, {'B': 111}, {'A': 182, 'C': 'das'}])
        assert txt.data == [
            {'A': 123, 'B': None, 'C': None},
            {'A': None, 'B': 111, 'C': None},
            {'A': 182, 'B': None, 'C': 'das'},
        ]

    def test_insert_dict_of_lists(self):
        txt = TxtData()
        txt.insert(
            {
                'A': [123, None, 182],
                'B': [None, 111, None],
                'C': [None, None, 'das'],
            }
        )
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

    def test_filter_single_arg(self):
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

    def test_filter_mult_arg(self):
        data = [
            {'A': None, 'B': 10, 'C': 50},
            {'A': 150, 'B': 50, 'C': 39},
            {'A': 32, 'B': 50, 'C': 2},
        ]

        txt = TxtData(data)
        filtered_txt = txt.filter(A=150, B=10)
        assert len(filtered_txt) == 2

    def test_delete(self):
        data = [
            {'A': 10, 'B': 50, 'C': 'asd'},
            {'A': None, 'B': 10, 'C': 50},
            {'A': 150, 'B': 50, 'C': 39},
            {'A': 123, 'B': 33, 'C': 12},
            {'A': 55, 'B': None, 'C': 44},
            {'A': 32, 'B': 50, 'C': 2},
        ]
        txt = TxtData(data)
        txt.delete(A=None, B=50)
        assert txt.data == [
            {'A': 123, 'B': 33, 'C': 12},
            {'A': 55, 'B': None, 'C': 44},
        ]

    def test_to_dicts(self):
        data = _random_sample()
        txt = TxtData(data)
        assert txt.to_dicts() == data
