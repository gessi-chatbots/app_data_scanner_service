import json, requests, time, signal

def handler(signum, frame):
    print("*****TIMEOUT EXCEPTION*****")
    raise Exception("It took too much time to end that")

def call_service(url, it_apps, responses):
    #signal.signal(signal.SIGALRM, handler)
    #signal.alarm(600)
    r = requests.post(url, json=json.dumps(it_apps), headers={"Content-type":"application/json"})
    #signal.alarm(0)
    responses.append(r.json())
file = open('data/query/MApp-KG-query-2.0.json')

apps = json.load(file)

i = 0
responses = []
while i < len(apps):
    it_apps = []
    it_apps.append(apps[i])

    url = "http://127.0.0.1:5500/export-data?api-consumers=true&web-scrapers=true"

    try:
        call_service(url, it_apps, responses)
    except Exception as e:
        try:
            call_service(url, it_apps, responses)
        except Exception as e:
            print(e)
            missed_apps = None
            with open("../data/scanApps/fail/missed-apps.json") as f1:
                missed_apps = json.load(f1)
                missed_apps.append(it_apps[0])
            with open("../data/scanApps/fail/missed-apps.json", 'w') as outfile:
                json.dump(missed_apps, outfile)

    i += 1
    if i % 10 == 0 and i > 0:
        time.sleep(10)

    perc = i / len(apps) * 100
    print("Completed " + str(perc) + "% (" + str(i) + "/" + str(len(apps)) + ")")

print(responses)