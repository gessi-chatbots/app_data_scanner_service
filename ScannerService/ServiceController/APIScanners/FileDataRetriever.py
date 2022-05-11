import json
import os

from ScannerService.ServiceController.APIScanners.IDataRetriever import IDataRetriever


class FileDataRetriever(IDataRetriever):

    def __init__(self):
        self.path = os.getcwd() + os.sep

    def get_data(self, app_name: str):
        file_route = self.path + app_name + ".json"
        with open(file_route) as file:
            return json.load(file)

