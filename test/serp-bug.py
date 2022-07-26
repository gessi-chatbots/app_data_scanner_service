from random import randint
import requests

success = 0
failure = 0
api_key = "81b9887924b7d5fceb209a510cb433b53e519e1a86f334dffd3c0b073967129c"
endpoint_sample = 'https://serpapi.com/search.json?engine=google_play&gl=us&hl=en&store=apps&no_cache=true&api_key='
search_term = "geolocation"

for result in range(0, 100):
    target = requests.get(endpoint_sample + api_key + "&q=" + search_term)
    result = target.json()
    random_chooser = randint(0, 5)
    
    try:
        print(str(success) + '- ' + result['organic_results'][0]["items"][random_chooser]['title'])
        success += 1
        
    except KeyError:
            failure += 1
            print(result['error'])

print(success)
print(failure)