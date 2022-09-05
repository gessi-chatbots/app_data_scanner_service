import json, requests, time

file = open('../data/app_query_MERGED.json')

apps = json.load(file)

i = 0
responses = []
while i < len(apps):
    it_apps = []
    for x in range(i, i+10):
        if (x < len(apps)):
            it_apps.append(apps[x])
    i += 10

    url = "http://127.0.0.1:5000/export-data?api-consumers=true&web-scrapers=true"
    r = requests.post(url, json=json.dumps(it_apps), headers={"Content-type":"application/json"})
    responses.append(r.json())
    time.sleep(10)

print(responses)