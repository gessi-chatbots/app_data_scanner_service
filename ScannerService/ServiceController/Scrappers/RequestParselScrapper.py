
import requests
from parsel import Selector

from ScannerService.ServiceController.Scrappers.Scrapper import Scrapper


class RequestParselScrapper(Scrapper):

    def __init__(self):
        super().__init__()

    def scrapWebsite(self, app_list, website_list):
        app_features_list = []
        for i in range(len(website_list)):
            req = requests.get(website_list[i])
            sel = Selector(text=req.text)
            relevant_info = sel.xpath('//ul[contains(@class,"badges link-color")]')
            data = {
                'features': relevant_info.css('a::text').getall(),
                'tags': relevant_info.css('span::text').getall()
            }
            app_features_list.append(data)
        return app_features_list
