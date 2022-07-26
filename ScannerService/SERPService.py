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
            "api_key": self._api_key,
            "no_cache": "True"
        }

    def get_data(self, app_name: str):
        self.cleanCall()
        self._params['product_id'] = app_name
        self._params['engine'] = 'google_play_product'
        return self.callAPI()

    def i_query_data(self, query, next_page_token):
        current_app.logger.info('Paginating for ' + query + ' (next_page_token: ' + next_page_token + ')')
        self._params['next_page_token'] = next_page_token
        res = [self.callAPI()]
        if 'serpapi_pagination' in res[0].keys():
            next_page_token = res[0]['serpapi_pagination']['next_page_token']
            res = res + self.i_query_data(query, next_page_token)
        return res

    def query_data(self, q):
        results = {}
        for string in q:
            self.cleanCall()
            current_app.logger.info("Looking for " + string + " apps in SERP API...")
            self._params['q'] = string
            self._params['engine'] = 'google_play'
            #current_app.logger.debug(self.callAPI())
            results[string] = [self.callAPI()]
            if 'serpapi_pagination' in results[string][0].keys():
                next_page_token = results[string][0]['serpapi_pagination']['next_page_token']
                results[string] = results[string] + self.i_query_data(string, next_page_token)
        return results

    def cleanCall(self):
        self._params['product_id'] = ''
        self._params['q'] = ''
        self._params['engine'] = ''
        if 'next_page_token' in self._params.keys():
            self._params.pop('next_page_token')

    def callAPI(self):
        search = GoogleSearch(self._params)
        result = search.get_dict()
        if 'error' in result.keys():
            current_app.logger.error(result['error'])
        return result