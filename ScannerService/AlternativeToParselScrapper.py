import requests
import privacypass
from parsel import Selector
from bs4 import BeautifulSoup

from ScannerService.Scrapper import Scrapper

import cloudscraper
import time
from flask import current_app

from fake_useragent import UserAgent


HOST = 'https://web.archive.org/'

HOST_HEAD = HOST + 'web/https://alternativeto.net/software/'
HOST_TAIL = '/about/'

HOST_QUERY = HOST + 'web/https://alternativeto.net/tag/'
HOST_QUERY_TAIL = '?sort=likes'

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

    def __queryWebsiteI(self, url, soup, page):

        apps = soup.find_all(itemprop='name')

        app_list = []
        for app in apps:
                app_name = app.text

                try:

                    url = HOST + app.get('href')
                    scraper = cloudscraper.create_scraper() 

                    ua = UserAgent().random
                    headers = {
                        'User-Agent': ua,
                    }

                    req = scraper.get(url, headers=headers)

                    time.sleep(5)  # suspend execution for 5 secs

                    soup = BeautifulSoup(req.text, 'html.parser')
                    link = soup.find(attrs={'data-link-action': 'AppStores Link'})

                    if link is not None:
                        if 'itunes' in link.get('href'):
                            current_app.logger.info('Ignoring ' + app_name + ' (iOS app)')
                        else:
                            package = link.get('href').split('id=')[1]
                            app_list.append({'name': app_name, 'package': package})
                            current_app.logger.info('Scrapped app: {app_name: \'' + app_name + '\', package = \'' + package + '\'}')
                    else:
                        current_app.logger.error('Ignoring ' + app_name + ' (no package was found)')

                except Exception as e: 
                    print(e)
                    current_app.logger.error("Network error. App " + app_name + " could not be extracted")


        # Pagination is implemented - however, the wayback machine usually does not have pages in their storage
        try:

            page = page + 1

            next_page = url + '&p=' + str(page)
            current_app.logger.info("trying pagination to " + next_page)
            scraper = cloudscraper.create_scraper() 
            req = scraper.get(next_page)

            if req.status_code != 404:

                soup = BeautifulSoup(req.text, 'html.parser')
                current_app.logger.info("success! let's go")
                app_list = app_list + self.__queryWebsiteI(url, soup, page)

            else:
                current_app.logger.info("No more pages")

        except Exception as e:
            print(e)
            current_app.logger.info("No more pages")

        return app_list

    def queryWebsite(self, q):
        app_list = []
        for query in q:

            url = HOST_QUERY + query + HOST_QUERY_TAIL
            scraper = cloudscraper.create_scraper() 
            req = scraper.get(url)

            soup = BeautifulSoup(req.text, 'html.parser')

            #get apps

            app_list = app_list + self.__queryWebsiteI(url, soup, 1)
        return app_list
