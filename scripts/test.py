import requests
import privacypass
import cloudscraper
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def send_request(session, proxy, url):
    try:
        #User-Agent
        ua = UserAgent().random
        headers = {
            'User-Agent': ua,
        }
        response = session.get(url, proxies={'https': f"https://{proxy}"}, headers=headers, timeout=30)

        soup = BeautifulSoup(response.text, 'html.parser')
        apps = soup.find_all(class_='Heading_h2__7oYDQ')
        print(str(response.status_code))
        print(str(len(apps) )+ " apps")
        for app in apps:
            print(app.text)
    except Exception as e: 
        print("Connection error")
        print(e)        

#Call set-up
url = 'https://alternativeto.net/browse/search/?q=Run Tracker'

with open('list_proxy.txt', 'r') as file:
       proxies = file.readlines()
       with requests.Session() as session:
           for proxy in proxies:
               send_request(session, proxy, url)

#scraper = cloudscraper.create_scraper() 
#req = scraper.get(url, headers=headers)
#req = requests.get(url, proxies=proxies)



