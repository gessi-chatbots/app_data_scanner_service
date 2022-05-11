from unittest import TestCase

from ScannerService.ServiceController.APIScanners.GPSAPI import GPSAPI


class TestGPSAPI(TestCase):
    def setUp(self):
        self.example_dict = {
            'A': 'A',
            'B': 'B',
            'C': 'C',
            'D': 'D',
            'E': 'E'
            }
        self.example_keys = ['A', 'C', 'D']

    def test_extract_info(self):
        result = GPSAPI.extract_info(self.example_dict,self.example_keys)
        self.assertDictEqual(result, {
            'A': 'A',
            'C': 'C',
            'D': 'D'
            })
