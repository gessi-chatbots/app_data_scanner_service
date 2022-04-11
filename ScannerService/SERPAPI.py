from ScannerService.APIScanner import APIScanner
from ScannerService.FileDataRetriever import FileDataRetriever
from ScannerService.SERPService import SERPService


class SERPAPI(APIScanner):

    def __init__(self, keys):
        super().__init__(local_data_source=FileDataRetriever(), remote_data_source=SERPService(), keys_to_extract=keys)

    def scanAppData(self, app_list):
        app_info_list = []
        for app in app_list:
            results = {}
            try:
                results = self._local_data_source.get_data(app)
            except FileNotFoundError:
                results = self._remote_data_source.get_data(app)
            app_info = self.extract_data(results, self._keys)
            app_info_list.append(self.prettify(app_info))
        return app_info_list

    @staticmethod
    def extract_data(api_results, _keys):
        extracted_info = {}
        for _key in _keys:
            aux = list(SERPAPI.find(api_results, _key))
            extracted_info[_key] = aux
        return SERPAPI.prettify(extracted_info)

    @staticmethod
    def find(api_results, _key):
        if type(api_results) == dict:
            if _key in api_results.keys():
                yield api_results[_key]
            for element in api_results.values():
                for x in SERPAPI.find(element, _key):
                    yield x

        if type(api_results) == list:
            for element in api_results:
                for x in SERPAPI.find(element, _key):
                    yield x

    @staticmethod
    def prettify(app_info):
        new_dict = {}
        for key_ in app_info.keys():
            if len(app_info[key_]) == 1:
                new_dict[key_] = app_info[key_][0]
            else:
                aux_list = []
                for element in app_info[key_]:
                    if type(element) is not list:
                        aux_list.append(element)
                    else:
                        aux_list += element
                new_dict[key_] = aux_list
        return new_dict
