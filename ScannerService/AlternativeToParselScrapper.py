import requests
from parsel import Selector
from bs4 import BeautifulSoup

from ScannerService.Scrapper import Scrapper
from ScannerService.Utils import Utils

import cloudscraper
import time
from flask import current_app
import itertools

from fake_useragent import UserAgent


HOST = 'https://web.archive.org/'
HOST_HEAD = HOST + 'web/https://alternativeto.net/software/'
HOST_TAIL = '/about/'
HOST_QUERY = HOST + 'web/https://alternativeto.net/tag/'
HOST_QUERY_TAIL = '?sort=likes'

class AlternativeToParselScrapper(Scrapper):

    def __init__(self):
        super().__init__()

    def scrapWebsite(self, app, context, review_days_old=365):

        context.logger.info("Looking for " + app['package'] + " in AlternativeTo...")

        #names are hard to manage - generating multiple combinations
        name = self.sanitize_name(app['name'])

        success, req = Utils.rotateAlternativeToNames(name, HOST_HEAD, HOST_TAIL, context)
        
        if success:
            sel = Selector(text=req.text)

            relevant_info = sel.xpath('//ul[contains(@class,"badges link-color")]')
            open_source = sel.xpath('//ul[contains(@class,"badges")]')
            app_name = sel.xpath('//h1').css('h1::text').getall()
            app_name = app_name[0] if len(app_name) > 0 else None
            summary = sel.xpath('//h2').css('span::text').getall()
            summary = summary[0] if len(summary) > 0 else None
            description = "\n".join(sel.xpath('//span[contains(@class, "server-content longForm formatHtml")]').css('span::text').getall())

            features_sel = relevant_info.css('a::text').getall()
            features = []
            for f in features_sel:
                features.append({'package': app['package'], 'name': f})

            data = {
                'features': features,
                'tags': relevant_info.css('span::text').getall(),
                'is_open_source': True if 'Open Source' in ','.join(open_source.css('span::text').getall()) else False,
                'app_name': app_name,
                'package_name': app['package'],
                'summary': summary,
                'description': description
            }
            return data
        else:
            context.logger.info('Couldn\'t find data of app ' + app['package'] + ' in AlternativeTo')

    def sanitize_name(self, name):
        x = name.find(' - ' )
        if x != -1:
            name = name[0:name.find(' - ')]

        x = name.find(': ')
        if x != -1:
            name = name[0:name.find(': ')]

        x = name.find(' by ')
        if x != -1:
            name = name[0:name.find(' by ')]

        name = name.replace('(','').replace(')','').replace('\'','').replace(',','')
        return name

    def __queryHost(self, req, app_list, app_name):
        soup = BeautifulSoup(req.text, 'html.parser')

        a_list = soup.find(class_='AppExternalLinks_appstoreContainer__2tZk-') 
        extra = soup.find(class_='AppExternalLinks_appstoreContainer__KwEhd')
        extra_2 = soup.find(class_='jsx-126216845 appstore-container')
        
        if a_list is None:
            a_list = []
        if extra is not None:
            a_list += extra
        if extra_2 is not None:
            a_list += extra_2

        #extra_links = soup.find(class_='site-links icon-official-website')
        #if extra_links is not None:
        #    print("that shit happened")
        #    a_list = a_list + extra_links


        if a_list is not None:
            links = [a.get('href') for a in a_list]
            link = next(x for x in links if 'play.google.com' in x or 'market.android.com' in x)

            #duplicate
            if link is not None:
                if 'itunes' in link:
                    current_app.logger.info('Ignoring ' + app_name + ' (iOS app)')
                else:
                    package = link.split('id=')[1].replace('&hl=en','')
                    app_list.append({'name': app_name, 'package': package})
                    current_app.logger.info('Scrapped app: {name: \'' + app_name + '\', package = \'' + package + '\'}')
            else:
                current_app.logger.error('Ignoring ' + app_name + ' (no Android package was found)')
        else:
            current_app.logger.error('Ignoring ' + app_name + ' (no Android package was found)')     

    def __queryWebsiteI(self, url, soup, page):

        apps = soup.find_all(itemprop='name')
        print(len(apps))

        app_list = []
        for app in apps:
                app_name = app.text

                try:

                    url = HOST + app.get('href')
                    scraper = cloudscraper.create_scraper() 

                    ua = UserAgent().random
                    headers = {
                        'User-Agent': ua,
                        'Connection': 'close'
                    }

                    req = scraper.get(url, headers=headers)

                    time.sleep(5)  # suspend execution for 5 secs

                    soup = BeautifulSoup(req.text, 'html.parser')
                    link = soup.find(attrs={'data-link-action': 'AppStores Link'})

                    if link is not None:
                        if 'itunes' in link.get('href'):
                            current_app.logger.info('Ignoring ' + app_name + ' (iOS app)')
                        else:
                            package = link.get('href').split('id=')[1].replace('&hl=en','')
                            app_list.append({'name': app_name, 'package': package})
                            current_app.logger.info('Scrapped app: {name: \'' + app_name + '\', package = \'' + package + '\'}')
                    else:
                        #No package found. Trying host page
                        name = app_name.replace(':','').replace('(','').replace(')','').replace('\'','').replace(',','')
                        whitespaced_names = name.split(' ')

                        names = []

                        #https://stackoverflow.com/questions/464864/how-to-get-all-possible-combinations-of-a-list-s-elements
                        for L in range(0, len(whitespaced_names)+1):
                            for subset in itertools.combinations(whitespaced_names, L):
                                if (len(subset) > 0):
                                    names.append("".join(subset))

                        #Normalize URL
                        success = False
                        i = 0
                        while not success and i < len(names):
                            url = HOST_HEAD + names[i] + HOST_TAIL
                            req = requests.get(url)
                            if req.status_code != 404:
                                success = True
                            else:
                                i += 1


                        if success:
                            self.__queryHost(req, app_list, app_name)
                        else:
                            current_app.logger.error('Ignoring ' + app_name + ' (no Android package was found)')     

                except Exception as e: 
                    current_app.logger.error("Network error. App " + app_name + " could not be extracted")


        # Pagination is implemented - however, the wayback machine usually does not have pages in their storage
        try:

            page = page + 1

            next_page = url + '&p=' + str(page)
            #current_app.logger.info("trying pagination to " + next_page)
            scraper = cloudscraper.create_scraper() 
            req = scraper.get(next_page, headers={'Connection':'close'})

            if req.status_code != 404:

                soup = BeautifulSoup(req.text, 'html.parser')
                current_app.logger.info("success! let's go")
                app_list = app_list + self.__queryWebsiteI(url, soup, page)

        except Exception as e:
            current_app.logger.info("No more pages")

        return app_list

    def __queryAlternativesToI(self, app_list, url, page):
        scraper = cloudscraper.create_scraper() 
        req = scraper.get(url + "?p=" + str(page))
        if req.status_code == 200:
            current_app.logger.info("Next page: " + req.url)
            soup = BeautifulSoup(req.text, 'html.parser')
            try:
                apps = soup.find_all(attrs={'data-testid': 'app-header'})
                app_names = []

                if len(apps) == 0:
                    apps = soup.find_all(attrs={'data-link-action': 'Alternatives'})
                    for app in apps:
                        app_names.append(app.get('href').split('alternativeto.net/software/')[1].split('/about')[0].replace("/",""))
                else:
                    for app in apps:
                        app_names.append(app.find('a').get('href').split('alternativeto.net/software/')[1].split('/about')[0].replace("/",""))

                for name in app_names:
                    try:
                        req = requests.get(HOST_HEAD + name + HOST_TAIL)
                        self.__queryHost(req, app_list, name)
                    except Exception as e:
                        current_app.logger.error('Ignoring ' + name + ' (no Android package was found)')

                self.__queryAlternativesToI(app_list, url, page+1)     

            except Exception as e:
                current_app.logger.error(e)
        else:
            current_app.logger.info("No more pages")

    def queryWebsite(self, q, apps):
        app_info = {}

        # Alternatives to

        for app in apps:
            current_app.logger.info('Querying alternatives to ' + app)
            url = HOST_HEAD + app

            app_list = []
            self.__queryAlternativesToI(app_list, url, 1)
            app_info[app] = app_list

        # Query

        for query in q:

            current_app.logger.info('Querying ' + query)
            url = HOST_QUERY + query.replace(' ','-') + HOST_QUERY_TAIL
            scraper = cloudscraper.create_scraper() 
            req = scraper.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')

            #get apps

            app_list = self.__queryWebsiteI(url, soup, 1)

            app_info[query] = app_list

        return app_info
