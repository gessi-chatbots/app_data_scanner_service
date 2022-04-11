from serpapi import GoogleSearch

from ScannerService.IDataRetriever import IDataRetriever
from ScannerService.settings import DEFAULT_API_KEY


class SERPService(IDataRetriever):

    def __init__(self, api_key=DEFAULT_API_KEY):
        self._api_key = api_key
        self._params = {
            "engine": "google_play_product",
            "store": "apps",
            "product_id": '',
            "api_key": self._api_key
        }

    def get_data(self, app_name: str):
        self._params['product_id'] = app_name
        search = GoogleSearch(self._params)
        result = search.get_dict()
        if 'error' in result.keys():
            raise Exception
        return result
