from ScannerService.APIScanner import APIScanner

from ScannerService.FileDataRetriever import FileDataRetriever
from ScannerService.GPSService import GPSService

from flask import current_app

import multiprocessing
from ScannerService.settings import GOOGLE_PLAY_CATEGORIES


class GPSAPI(APIScanner):

    def __init__(self, info):
        super().__init__(local_data_source=FileDataRetriever(), remote_data_source=GPSService(), keys_to_extract=info)

    def scanAppData(self, app, context, review_days_old, include_reviews=True, review_number=50):

        context.logger.info("Looking for " + app + " in GPS API...")
        result = {}
        
        result = self._remote_data_source.get_data(app, review_days_old)

        if result is not None:
            relevant_info = self.extract_info(result, relevant_keys=self._keys)
            return relevant_info

    def queryAppData(self, q):
        app_info_list = {}
        for query in q:
            app_info_list[query] = self._remote_data_source.queryAppData(query)
        return app_info_list
    
    def queryAppDataByCategories(self, context):
        app_info_list = []
        for category in GOOGLE_PLAY_CATEGORIES:
            if 'GAME' not in category['cat_key']: 
                app_info_list.extend(self._remote_data_source.queryAppData(category['cat_key']))
        
        # Convert dictionaries to tuples for hashing and comparison
        tuple_array = [tuple(sorted(d.items())) for d in app_info_list]
        # Remove duplicates using a set
        unique_tuples = set(tuple_array)
        # Convert tuples back to dictionaries
        unique_dicts = [dict(t) for t in unique_tuples]
        context.logger.info(str(len(unique_dicts)) + " apps found")
        return unique_dicts

    @staticmethod
    def extract_info(data, relevant_keys):
        result = {}
        for key in relevant_keys:
            if key is not None and key in data:
                result[key] = data[key]
        return result
