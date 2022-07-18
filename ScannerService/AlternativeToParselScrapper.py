
import requests
from parsel import Selector

from ScannerService.Scrapper import Scrapper

HOST_HEAD = 'https://web.archive.org/web/https://alternativeto.net/software/'
HOST_TAIL = '/about/'

class AlternativeToParselScrapper(Scrapper):

    def __init__(self):
        super().__init__()

    def scrapWebsite(self, app_list):
        app_features_list = []
        for app in app_list:
            url = HOST_HEAD + app + HOST_TAIL
            req = requests.get(url)
            sel = Selector(text=req.text)
            relevant_info = sel.xpath('//ul[contains(@class,"badges link-color")]')
            data = {
                'features': relevant_info.css('a::text').getall(),
                'tags': relevant_info.css('span::text').getall()
            }
            app_features_list.append(data)
        return app_features_list
