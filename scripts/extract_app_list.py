import json

import csv

a = ""

with open('../data/keywords.csv', 'r') as file:
    a = file.read().rstrip()

f_serp = open('../data/app_query_serp_results.json')
f_gps = open('../data/app_query_gps_results.json')
f_fdroid = open('../data/app_query_fdroid_results.json')

data_serp = json.load(f_serp)
data_gps = json.load(f_gps)
data_fdroid = json.load(f_fdroid)

print("APP DATA CONSOLIDATION")
print("# keywords = " + str(len(a)) + "\n")

print("*****************")
print("***GOOGLE PLAY***")
print("*****************\n")

print("Total number of results (SERP): " + str(len(data_serp)))
print("Total number of results (GPS): " + str(len(data_gps)) + "\n")

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

print("Unique apps (SERP): " + str(len(unique_serp)))
print("Unique apps (GPS): " + str(len(unique_gps)) + "\n")

merged_res = unique_serp + unique_gps

unique_gp_merged = list({ each['package'] : each for each in merged_res }.values())

print("Unique apps (SERP + GPS) " + str(len(unique_gp_merged)) + "\n")

#with open('../data/app_query_results_parsed.json', 'w') as out:
#	json.dump(res, out)

#f.close()

#print(unique_merged)

f_serp.close()
f_gps.close()

print("********************")
print("***ALTERNATIVE TO***")
print("********************\n")


print("{To be done}\n")
#TODO

print("********************")
print("******F-DROID*******")
print("********************\n")

print("Total number of results (F-DROID): " + str(len(data_fdroid)))
unique_fdroid = list({ each['package'] : each for each in data_fdroid }.values())
print("Unique apps (F-DROID): " + str(len(unique_fdroid)) + "\n")

print("*******************")
print("***CONSOLIDATION***")
print("*******************\n")

all_merged = unique_gp_merged + unique_fdroid
print("Total number of results (ALL): " + str(len(all_merged)))
unique_all = list({ each['package'] : each for each in all_merged }.values())
print("Unique apps (ALL): " + str(len(unique_all)) + "\n")

#TODO