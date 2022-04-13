from unittest import TestCase

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
            '2': 2,
            '3': 3,
            '5': 5
        }
        self.assertDictEqual(res, result, "Error")

    def test_find(self):
        res1 = SERPAPI.find(self.example_dict, '3')
        res2 = SERPAPI.find(self.example_dict, 'B')
        self.assertEqual(res1, 3)
        self.assertDictEqual(res2, {'3': 3})