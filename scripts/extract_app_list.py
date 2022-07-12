import json

f = open('../data/app_query_results.json')

data = json.load(f)

print("Total number of results: " + str(len(data)))

x = 0

res = []

for key in data.keys():
	for results in data[key]['organic_results']:
		#We ignore 'Similar apps'
		if 'title' not in results or results['title'] == 'More results':
			#TODO: organic flat results
			x += len(results['items'])
			for app in results['items']:
				res.append({'name': app['title'], 'package': app['link'].split('?id=')[1]})

print("We found " + str(x) + " apps in Google Play")

with open('../data/app_query_results_parsed.json', 'w') as out:
	json.dump(res, out)

f.close()
