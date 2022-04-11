from unittest import TestCase

import ScannerService
from ScannerService.SERPAPI import SERPAPI


class TestSERPAPI(TestCase):
    def setUp(self):
        self.example_dict = {
            'A': {
                '1': 1,
                '2': 2,
                'B': {
                    '3': 3
                },
                'C': {
                    '3': 31
                }
            },
            'D': 5,
            'E': {
                '4': 4,
                '5': 5,
                '2': 21
            }
        }
        self.example_keys = ['2', '3', '5']

    def test_extract_data(self):
        res = SERPAPI.extract_data(self.example_dict, self.example_keys)
        result = {
            '2': [2, 21],
            '3': [3, 31],
            '5': 5
        }
        self.assertDictEqual(res, result, "Error")

    def test_find(self):
        res1 = list(SERPAPI.find(self.example_dict, '3'))
        res2 = list(SERPAPI.find(self.example_dict, 'B'))

        self.assertListEqual(res1, [3, 31])
        self.assertListEqual(res2, [{'3': 3}])

    def test_prettify(self):
        input_ = {
            '2': [2, 21],
            '3': [3, 31],
            '5': [5],
            '6': [[2, 5],
                  [1, 3]]
        }
        output_ = SERPAPI.prettify(input_)
        self.assertDictEqual(output_, {'2': [2, 21],
                                       '3': [3, 31],
                                       '5': 5,
                                       '6': [2, 5, 1, 3]})
