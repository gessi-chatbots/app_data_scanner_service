import requests
import privacypass
from parsel import Selector
from bs4 import BeautifulSoup

from ScannerService.Scrapper import Scrapper

import cloudscraper
from flask import current_app


HOST_HEAD = 'https://web.archive.org/web/https://alternativeto.net/software/'
HOST_TAIL = '/about/'

HOST_QUERY = 'https://web.archive.org/web/https://alternativeto.net/tag/'

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

    def queryWebsite(self, q):
        app_list = []
        for query in q:
            url = HOST_QUERY + query
            req = requests.get(url)

            scraper = cloudscraper.create_scraper() 
            req = scraper.get(url)

            soup = BeautifulSoup(req.text, 'html.parser')

            apps = soup.find_all(itemtype='http://schema.org/SoftwareApplication')
            print(url + " (" + str(req.status_code) + "): " + str(len(apps)) + " apps")

            for app in apps:
                print(app
                    #.get(class_='col-xs-9 ').get('h3').get('a').get('href')
                    )
