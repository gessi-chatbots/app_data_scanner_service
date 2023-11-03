import json

with open("..\..\data\wiki-query.json") as f1:
    apps = json.load(f1)

    formatted_apps = []

    for app in apps:
        formatted_app = {'name': app['itemLabel'], 'package': app['package']}
        formatted_apps.append(formatted_app)

    with open("..\..\data\wiki-query-formatted.json", 'w') as outfile:
        json.dump(formatted_apps, outfile)