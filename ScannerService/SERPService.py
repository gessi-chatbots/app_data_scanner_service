import flatdict
from serpapi import GoogleSearch

from ScannerService.IDataRetriever import IDataRetriever
from ScannerService.settings import DEFAULT_API_KEY

from flask import current_app


class SERPService(IDataRetriever):

    def __init__(self, api_key=DEFAULT_API_KEY):
        self._api_key = api_key
        self._params = {
            "engine": "google_play_product",
            "store": "apps",
            "product_id": '',
            "q": '',
            "api_key": self._api_key
        }

    def get_data(self, app_name: str):
        self.cleanCall()
        self._params['product_id'] = app_name
        self._params['engine'] = 'google_play_product'
        return callAPI()

    def query_data(self, q):
        self.cleanCall()
        results = {}
        for string in q:
            current_app.logger.info("Looking for " + string + " apps in SERP API...")
            self._params['q'] = string
            self._params['engine'] = 'google_play'
            #current_app.logger.debug(self.callAPI())
            results[string] = self.callAPI()
        return results

    def cleanCall(self):
        self._params['product_id'] = ''
        self._params['q'] = ''
        self._params['engine'] = ''

    def callAPI(self):
        search = GoogleSearch(self._params)
        result = search.get_dict()
        if 'error' in result.keys():
            current_app.logger.info(result)
            raise Exception
        return result