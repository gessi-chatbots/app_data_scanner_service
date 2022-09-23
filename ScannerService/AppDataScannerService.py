from ScannerService.GPSAPI import GPSAPI
from ScannerService.SERPAPI import SERPAPI

from ScannerService.AlternativeToParselScrapper import AlternativeToParselScrapper
from ScannerService.FDroidScrapper import FDroidScrapper

from ScannerService.settings import GPS_KEYS, SERP_KEYS, NEEDED_INFO, PRIORITY_LIST, INFO_MATRIX

from flask import current_app

import json, uuid, numpy

class AppDataScannerService:

    app_info = []

    def __init__(self):
        self._api_list = [GPSAPI(GPS_KEYS), SERPAPI(SERP_KEYS)]
        self._scrapper_list = [AlternativeToParselScrapper(),FDroidScrapper()]

    #background function for scanning apps - Applies observer pattern
    def scanApps(self, request_id, app_list, api_consumers, web_scrapers, context):
        self.app_info = []
        #API Scanners typically only require packages
        for app in app_list:
            temp_list = []
            if api_consumers is True:
                context.logger.info("Running API consumers...")
                self.runApiScanners(app['package'], context, temp_list)
            #Websites require either packages or names
            if web_scrapers is True:
                context.logger.info("Running web scrapers...")
                self.runWebScrappers(app, context, temp_list)

            self.format_data(temp_list)
        
        file = 'data/scanApps/' + str(request_id) + '.json'
        with open(file, 'w') as app_file:
            json.dump(self.app_info, app_file)

    def runAppDataScanning(self, app_list, api_consumers, web_scrapers):
        # We create a unique ID for this request
        request_id = uuid.uuid4()
        self.scanApps(request_id, app_list, api_consumers, web_scrapers, current_app._get_current_object())
        return str(request_id)

    def runAppDataQuery(self, api, q, apps):
        if api == 'serp':
            return self._api_list[1].queryAppData(q + apps)
        elif api == 'gps':
            return self._api_list[0].queryAppData(q + apps)
        else:
            current_app.logger.error("No API to run this query")

    def runAppDataQueryScrapper(self, site, q, apps):
        if site == 'alternative-to':
            return self._scrapper_list[0].queryWebsite(q, apps)
        elif site == 'fdroid':
            return self._scrapper_list[1].queryWebsite(q + apps)
        else:
            current_app.logger.error("No SITE to run this query")

    def runAppDataScrapper(self, site, app_list):
        if site == 'alternative-to':
            return self._scrapper_list[0].scrapWebsite(app_list)
        else:
            current_app.logger.error("No SITE to run this scrapper")

    def getAppScannedData(self):
        return self.app_info

    def runApiScanners(self, app, context, temp_list):
        for api_scanner in self._api_list:
            temp_list.append(api_scanner.scanAppData(app, context))
        # for i in range(len(app_list)):
        #     app_data = {}
        #     aux_list = []
        #     for j in range(len(self._api_list)):
        #         if len(temp_list[j]) > i:
        #             aux_list.append(temp_list[j][i])
        #         else:
        #             aux_list.append({})
        #     for item in PRIORITY_LIST.keys():
        #         app_data[item] = AppDataScannerService.get_value(item, aux_list)
        #     self.app_info.append(app_data)

    def runWebScrappers(self, app, context, temp_list):
        
        for scrapper in self._scrapper_list:
            res = scrapper.scrapWebsite(app, context)
            temp_list.append(res)
            # for i in range(len(res)):
            #     if i < len(self.app_info):
            #         self.app_info[i] = {**self.app_info[i], **res[i]}
            #     else:
            #         self.app_info.append(res[i])
            #     if 'package' not in self.app_info[i].keys():
            #         self.app_info[i] = {**app_names[i], **self.app_info[i]}

    def format_data(self, temp_list):
        app = {}
        for item in PRIORITY_LIST.keys():
            app[item] = AppDataScannerService.get_value(item, temp_list)
        self.app_info.append(app)

    @staticmethod
    def find_element(element):
        for i in range(len(NEEDED_INFO)):
            if NEEDED_INFO[i] == element:
                return i

    @staticmethod
    def get_value(_item, _info_list):

        priority_indices = numpy.argsort(PRIORITY_LIST[_item])[::-1]

        for index in priority_indices:

            # index of the preferred data source
            preferred = index
            # index of the data item in the list of relevant data fields
            index = AppDataScannerService.find_element(_item)
            # index of the data item in the data source list
            element = INFO_MATRIX[preferred][index]

            # we look for the preferred value only if it is not None
            if element is not None and _info_list[preferred] is not None:
                if element in _info_list[preferred].keys() and _info_list[preferred][element] is not None:              
                    return _info_list[preferred][element]
        
        return None

        # found = False
        # i = 0
        # while not found and i < len(PRIORITY_LIST[_item]):

        #     preferred = PRIORITY_LIST[_item][i]
        #     index = AppDataScannerService.find_element(_item)
        #     element = INFO_MATRIX[preferred][index]

        #     if element is not None:
        #         if element in _info_list[preferred].keys() and _info_list[preferred][element] is not None:
        #             return _info_list[preferred][element]

        #     i += 1
        # return None
