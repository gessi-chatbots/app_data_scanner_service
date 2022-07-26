from ScannerService.GPSAPI import GPSAPI
from ScannerService.SERPAPI import SERPAPI

from ScannerService.AlternativeToParselScrapper import AlternativeToParselScrapper
from ScannerService.FDroidScrapper import FDroidScrapper

from ScannerService.settings import GPS_KEYS, SERP_KEYS, NEEDED_INFO, PRIORITY_LIST, INFO_MATRIX

from flask import current_app

class AppDataScannerService:
    app_info = []

    def __init__(self):
        self._api_list = [GPSAPI(GPS_KEYS), SERPAPI(SERP_KEYS)]
        self._scrapper_list = [AlternativeToParselScrapper(),FDroidScrapper()]

    def runAppDataScanning(self, app_list):
        self.runApiScanners(list({ each['package'] : each for each in app_list }))
        self.runWebScrappers(list({ each['name'] : each for each in app_list }))

    def runAppDataQuery(self, api, q):
        if api == 'serp':
            return self._api_list[1].queryAppData(q)
        elif api == 'gps':
            return self._api_list[0].queryAppData(q)
        else:
            current_app.logger.error("No API to run this query")

    def runAppDataQueryScrapper(self, site, q):
        if site == 'alternative-to':
            return self._scrapper_list[0].queryWebsite(q)
        elif site == 'fdroid':
            return self._scrapper_list[1].queryWebsite(q)
        else:
            current_app.logger.error("No SITE to run this query")

    def runAppDataScrapper(self, site, app_list):
        if site == 'alternative-to':
            return self._scrapper_list[0].scrapWebsite(app_list)
        else:
            current_app.logger.error("No SITE to run this scrapper")

    def getAppScannedData(self):
        return self.app_info

    def runApiScanners(self, app_list):
        temp_list = []
        for api_scanner in self._api_list:
            temp_list.append(api_scanner.scanAppData(app_list))
        for i in range(len(app_list)):
            app_data = {}
            aux_list = []
            for j in range(len(self._api_list)):
                aux_list.append(temp_list[j][i])
            for item in PRIORITY_LIST.keys():
                app_data[item] = AppDataScannerService.get_value(item, aux_list)
            self.app_info.append(app_data)

    def runWebScrappers(self, app_names):
        #TODO generalize for all available scrappers
        website_list = []
        #for app in app_names:
        #    # hardcoded for now
        #    website = 'https://web.archive.org/web/https://alternativeto.net/software/' + app + '/about/'
        #    website_list.append(website)
        for scrapper in self._scrapper_list:
            res = scrapper.scrapWebsite(app_list=app_names)
            for i in range(len(res)):
                self.app_info[i] = {**self.app_info[i], **res[i]}

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
