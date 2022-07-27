import requests
from parsel import Selector
from bs4 import BeautifulSoup

from ScannerService.Scrapper import Scrapper

from flask import current_app

HOST_QUERY = 'https://search.f-droid.org/?lang=en&q='

class FDroidScrapper(Scrapper):

    def __init__(self):
        super().__init__()

    def scrapWebsite(self, app_list):
        app_list = []
        #todo
        return app_list

    def queryWebsite(self, q):
        current_app.logger.info('Scrapping F-Droid for querying apps')
        app_info = {}
        for query in q:
            app_list = self.__queryAndPaginate(query)
            app_info[query] = app_list

        return app_info

    def __queryAndPaginate(self, query):
        app_list = []

        current_app.logger.info('Next query: ' + query)

        url = HOST_QUERY + query
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        apps = soup.find_all(class_='package-header')
        for app in apps:
            app_package = app.get('href').split('packages/')[1]
            app_name = app.find(class_='package-name').text.strip()
            app_list.append({'name': app_name, 'package': app_package})

        #PAGINATION
        pages = soup.find(class_='pagination')
        if pages != None:
            pages = pages.find_all('a')
            
            nextPage = pages[len(pages)-1].get('href')
            nextPageInt = nextPage.split('page=')[1].split('&lang')[0]
            currentPageInt = 1 if 'page' not in query else query.split('page=')[1].split('&lang')[0]

            if 'page' not in query or nextPageInt > currentPageInt:
                current_app.logger.info("Found new pages for " + query)
                app_list = app_list + self.__queryAndPaginate(nextPage.split('?q=')[1])
            else:
                current_app.logger.info("No more pages for " + query)
        return app_list