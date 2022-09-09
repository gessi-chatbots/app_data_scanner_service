import json, requests, time, signal

def handler(signum, frame):
    print("*****TIMEOUT EXCEPTION*****")
    raise Exception("It took too much time to end that")

def call_service(url, it_apps, responses):
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)
    r = requests.post(url, json=json.dumps(it_apps), headers={"Content-type":"application/json"})
    signal.alarm(0)
    responses.append(r.json())

file = open('../data/app_query_MERGED_1.json')

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

    try:
        call_service(url, it_apps, responses)
    except Exception:
        try:
            call_service(url, it_apps, responses)
        except Exception:
            print("There was a problem with these apps: ")
            for app in it_apps:
                print(app)
            print("Please try again later")

    time.sleep(10)

print(responses)