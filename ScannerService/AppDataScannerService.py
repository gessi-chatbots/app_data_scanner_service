from ScannerService.GPSAPI import GPSAPI
from ScannerService.SERPAPI import SERPAPI
from ScannerService.settings import GPS_KEYS, SERP_KEYS, NEEDED_INFO, PRIORITY_LIST, INFO_MATRIX


class AppDataScannerService:
    app_info = []

    def __init__(self):
        self._api_list = [GPSAPI(GPS_KEYS), SERPAPI(SERP_KEYS)]

    def runAppDataScanning(self, app_list):
        temp_list = []
        for api_scanner in self._api_list:
            temp_list.append(api_scanner.scanAppData(app_list))
        for i in range(len(self._api_list)):
            app_data = {}
            aux_list = []
            for j in range(len(temp_list[0])):
                aux_list.append(temp_list[j][i])
            for item in PRIORITY_LIST.keys():
                app_data[item] = AppDataScannerService.get_value(item, aux_list)
            self.app_info.append(app_data)

    def getAppScannedData(self):
        return self.app_info

    @staticmethod
    def find_element(element):
        for i in range(len(NEEDED_INFO)):
            if NEEDED_INFO[i] == element:
                return i

    @staticmethod
    def get_value(_item, _info_list):
        found = False
        i = 0
        while not found and i < len(PRIORITY_LIST[_item]):
            preferred = PRIORITY_LIST[_item][i]
            index = AppDataScannerService.find_element(_item)
            element = INFO_MATRIX[preferred][index]
            if element is not None:
                if element in _info_list[preferred].keys() and _info_list[preferred][element] is not None:
                    return _info_list[preferred][element]
            i += 1
        return None
