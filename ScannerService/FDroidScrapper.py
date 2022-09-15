import requests
from parsel import Selector
from bs4 import BeautifulSoup

from ScannerService.Scrapper import Scrapper

from flask import current_app

HOST_QUERY = 'https://search.f-droid.org/?lang=en&q='
HOST_APP = 'https://f-droid.org/en/packages/'

class FDroidScrapper(Scrapper):

    def __init__(self):
        super().__init__()

    def scrapWebsite(self, app, context):
        context.logger.info("Looking for " + app['package'] + " in FDroid...")
        # http request to FDroid app site
        url = HOST_APP + app['package']
        req = requests.get(url)
        if req.status_code == 200:

            # format with scraper
            soup = BeautifulSoup(req.content, 'html.parser')

            # extract data
            app_name = soup.find(class_='package-name').text.strip()
            summary = soup.find(class_='package-summary').text.strip()
            changelog = None
            if soup.find(class_='package-whats-new') is not None:
                changelog = soup.find(class_='package-whats-new').find(dir='auto').text.strip()
            description = soup.find(class_='package-description').text.strip()
            package = app['package']

            developer = None
            if len(soup.select('a[href^=mailto]')) > 0:
                developer = soup.select('a[href^=mailto]')[0].text.strip()

            open_source = 'True'

            links = soup.find_all(class_='package-link')
            developer_site = None
            repository = None
            for link in links:
                if link.find('a').text == 'Website':
                    developer_site = link.find('a').get('href')
                if link.find('a').text == 'Source Code':
                    repository = link.find('a').get('href')

            version = soup.find(class_='package-version-header').find('a').get('name')
            current_version_release_date = soup.find(class_='package-version-header').text.strip().split("Added on ")[1]

            data = {
                'app_name': app_name,
                'package_name': package,
                'summary': summary,
                'changelog': changelog,
                'description': description,
                'is_open_source': open_source,
                'developer': developer,
                'developer_site': developer_site,
                'version': version,
                'current_version_release_date': current_version_release_date,
                'repository': repository
            }

            return data

        else:
            return {}

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