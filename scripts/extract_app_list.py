import json

import csv

a = ""

with open('../data/keywords.csv', 'r') as file:
    a = file.read().rstrip()

f_serp = open('../data/app_query_serp_results.json')
f_gps = open('../data/app_query_gps_results.json')

data_serp = json.load(f_serp)
data_gps = json.load(f_gps)

print("***GOOGLE PLAY***")
print("Total number of results (SERP): " + str(len(data_serp)))
print("Total number of results (GPS): " + str(len(data_gps)) + "\n")
print("Keyword set = {" + a + "}\n")

serp_res = []
gps_res = []

#Data from SERP API
for key in data_serp.keys():
	for results in data_serp[key]['organic_results']:
		#We ignore 'Similar apps'
		if 'title' not in results or results['title'] == 'More results':
			#TODO: organic flat results
			for app in results['items']:
				serp_res.append({'name': app['title'], 'package': app['link'].split('?id=')[1]})


for query in data_gps:
    for app in query:
        gps_res.append({'name': app['title'], 'package': app['appId']})


unique_serp = list({ each['package'] : each for each in serp_res }.values())
unique_gps = list({ each['package'] : each for each in gps_res }.values())

print("We found " + str(len(unique_serp)) + " apps in SERP API")
print("We found " + str(len(unique_gps)) + " apps in GPS API\n")

merged_res = unique_serp + unique_gps

unique_merged = list({ each['package'] : each for each in merged_res }.values())

print("We found " + str(len(unique_merged)) + " apps (SERP + GPS)")

#with open('../data/app_query_results_parsed.json', 'w') as out:
#	json.dump(res, out)

#f.close()

f_serp.close()
f_gps.close()


print("***ALTERNATIVE TO***")

#TODO

print("***F-DROID***")

#TODO