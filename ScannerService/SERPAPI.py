from serpapi import GoogleSearch

from ScannerService.APIScanner import APIScanner


class SERPAPI(APIScanner):

    def __init__(self, info, api_key):
        super().__init__()
        self.keys = info
        self.api_key = api_key
        self.url = "https://serpapi.com/search.json?engine=google_play_product&store=apps&product_id=com.osmand.plus&api_key" \
                   "=c37299287ba2119e26c4c8537f00db73ade879fff83c103adc3789394c68bb67 "
        self.params = {
            "engine": "google_play_product",
            "store": "apps",
            "product_id": None,
            "api_key": self.api_key
        }

    def scanAppData(self, app_list):
        app_info_list = []
        for app in app_list:
            self.params['product_id'] = app
            results = GoogleSearch(self.params).get_dict()
            if "error" in results.keys():
                raise Exception
            app_info = self.extract_data(results, self.keys)
            app_info_list.append(app_info)
        return app_info_list

    @staticmethod
    def extract_data(api_results, _keys):
        extracted_info = {}
        for _key in _keys:
            aux = list(api_results.find(api_results, _key))
            extracted_info[_key] = aux
        return extracted_info

    @staticmethod
    def find(api_results, _key):
        if type(api_results) == dict:
            if _key in api_results.keys():
                yield api_results[_key]
            for element in api_results.values():
                for x in api_results.find(element, _key):
                    yield x

        if type(api_results) == list:
            for element in api_results:
                for x in api_results.find(element, _key):
                    yield x
