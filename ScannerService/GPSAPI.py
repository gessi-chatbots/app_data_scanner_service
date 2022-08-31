from ScannerService.APIScanner import APIScanner

from ScannerService.FileDataRetriever import FileDataRetriever
from ScannerService.GPSService import GPSService

from flask import current_app

import multiprocessing

class GPSAPI(APIScanner):

    def __init__(self, info):
        super().__init__(local_data_source=FileDataRetriever(), remote_data_source=GPSService(), keys_to_extract=info)

    def scanAppData(self, app_list, context, include_reviews=True, review_number=50):
        app_info_list = []
        for package in app_list:
            context.logger.info("Looking for " + package + " in GPS API...")
            result = {}
            
            result = self._remote_data_source.get_data(package)

            if result is not None:
                relevant_info = self.extract_info(result, relevant_keys=self._keys)
                app_info_list.append(relevant_info)
        return app_info_list

    def queryAppData(self, q):
        app_info_list = {}
        for query in q:
            app_info_list[query] = self._remote_data_source.queryAppData(query)
        return app_info_list

    @staticmethod
    def extract_info(data, relevant_keys):
        result = {}
        for key in relevant_keys:
            if key is not None and key in data:
                result[key] = data[key]
        return result
