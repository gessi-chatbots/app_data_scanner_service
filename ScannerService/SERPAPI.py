import flatdict

from ScannerService.APIScanner import APIScanner
from ScannerService.FileDataRetriever import FileDataRetriever
from ScannerService.SERPService import SERPService


class SERPAPI(APIScanner):

    def __init__(self, keys):
        super().__init__(local_data_source=FileDataRetriever(), remote_data_source=SERPService(), keys_to_extract=keys)

    def scanAppData(self, app, context):
        results = {}
        #try:
        #    results = self._local_data_source.get_data(app+'_serp')
        #except FileNotFoundError:
        context.logger.info("Looking for " + app + " in SERP API...")
        results = self._remote_data_source.get_data(app)
        results = dict(flatdict.FlatDict(results, delimiter='.'))
        app_info = self.extract_data(results, self._keys)
        return app_info

    def queryAppData(self, q):
        results = self._remote_data_source.query_data(q)
        return results

    @staticmethod
    def extract_data(api_results, _keys):
        extracted_info = {}
        for _key in _keys:
            if _key is not None:
                aux = SERPAPI.find(api_results, _key)
                extracted_info[_key] = aux

        return extracted_info

    @staticmethod
    def find(api_results, _key):
        if type(api_results) == dict:
            if _key in api_results.keys():
                return api_results[_key]
            for element in api_results.keys():
                found = SERPAPI.find(api_results[element], _key)
                if found is not None:
                    return found

        if type(api_results) == list:
            for element in api_results:
                found = SERPAPI.find(element, _key)
                if found is not None:
                    return found
        return None
