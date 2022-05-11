from google_play_scraper.exceptions import NotFoundError

from ScannerService.ServiceController.APIScanners.APIScanner import APIScanner

from ScannerService.ServiceController.APIScanners.FileDataRetriever import FileDataRetriever
from ScannerService.ServiceController.APIScanners.GPSService import GPSService


class GPSAPI(APIScanner):

    def __init__(self, info):
        super().__init__(local_data_source=FileDataRetriever(), remote_data_source=GPSService(), keys_to_extract=info)

    def scanAppData(self, app_list, include_reviews=True, review_number=50):
        app_info_list = []
        for package in app_list:
            result = {}
            found_locally = True
            try:
                result = self._local_data_source.get_data(package)
            except FileNotFoundError:
                found_locally = False
            if not found_locally:
                try:
                    result = self._remote_data_source.get_data(package)
                except NotFoundError:
                    result = {}
            relevant_info = self.extract_info(result, relevant_keys=self._keys)
            app_info_list.append(relevant_info)
        return app_info_list

    @staticmethod
    def extract_info(data, relevant_keys):
        result = {}
        if not data:
            return result
        for key in relevant_keys:
            if key is not None:
                result[key] = data[key]
        return result
