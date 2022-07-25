import json

import csv

with open('../data/keywords.csv', 'r') as file:
    a = file.read().rstrip()

keywords = {}

with open('../data/app-category-keywords.csv', newline='') as file:

	reader = csv.reader(file)
	for row in reader:
		for i,x in enumerate(row):
			if i == 0:
				keywords[row[i]] = []
			else:
				keywords[row[0]].append(row[i])

f_serp = open('../data/app_query_serp_results.json')
f_gps = open('../data/app_query_gps_results.json')
f_fdroid = open('../data/app_query_fdroid_results.json')
f_alternativeto = open('../data/app_query_alternativeto_results.json')

data_serp = json.load(f_serp)
data_gps = json.load(f_gps)
data_fdroid = json.load(f_fdroid)
data_alternativeto = json.load(f_alternativeto)

print("APP DATA CONSOLIDATION")
print("# keywords = " + str(len(data_serp)) + "\n")

print("*****************")
print("***GOOGLE PLAY***")
print("*****************\n")


#Complete app list
serp_res = {}
gps_res = {}
fdroid_res = {}
alternativeto_res = {}

#Init dictionaries with app categories
for keyword in keywords:
	serp_res[keyword] = []
	gps_res[keyword] = []
	fdroid_res[keyword] = []
	alternativeto_res[keyword] = []

#Data from SERP API
for key in data_serp.keys():
	for results in data_serp[key]['organic_results']:
		#We ignore 'Similar apps'
		if 'title' not in results or results['title'] == 'More results':
			#TODO: organic flat results
			for app in results['items']:
				value = {'name': app['title'], 'package': app['link'].split('?id=')[1]}
				
				for category in keywords.keys():
					if key in keywords[category]:
						serp_res[category].append(value)

#Data from GPS API
for key in data_gps.keys():
	for app in data_gps[key]:
		value = {'name': app['title'], 'package': app['appId']}
		for category in keywords.keys():
			if key in keywords[category]:
				gps_res[category].append(value)

#Data from F-Droid
for key in data_fdroid.keys():
	for category in keywords.keys():
		if key in keywords[category]:
			fdroid_res[category] += data_fdroid[key]

#Dara from Alternative-To
for key in data_alternativeto.keys():
	for category in keywords.keys():
		if key in keywords[category]:
			alternativeto_res[category] += data_alternativeto[key]

#Unique synthesis

unique_serp = {}
unique_gps = {}
unique_merged = {}
unique_fdroid = {}
unique_alternativeto = {}

for category in keywords.keys():
	unique_serp[category] = list({ each['package'] : each for each in serp_res[category] }.values())
	unique_gps[category] = list({ each['package'] : each for each in gps_res[category] }.values())
	unique_fdroid[category] = list({ each['package'] : each for each in fdroid_res[category] }.values())
	unique_alternativeto[category] = list({ each['package'] : each for each in alternativeto_res[category] }.values())

	unique_merged[category] = unique_gps[category].copy()
	for app in unique_serp[category]:
		package = app['package']
		packages = list({ each['package'] : each for each in gps_res[category] })
		if package not in packages:
			unique_merged[category].append(app)

print("Total number of results (SERP): " + str(sum(len(apps) for apps in serp_res.values())))
print("Total number of results (GPS): " + str(sum(len(apps) for apps in gps_res.values())) + "\n")

unique_apps_serp = sum(len(apps) for apps in unique_serp.values())
unique_apps_gps = sum(len(apps) for apps in unique_gps.values())
unique_apps_merged = sum(len(apps) for apps in unique_merged.values())

print("Unique apps (SERP): " + str(unique_apps_serp))
print("Unique apps (GPS): " + str(unique_apps_gps) + "\n")


print("Unique apps (Google Play [SERP+GPS]): " + str(unique_apps_merged) + "\n")


print("********************")
print("***ALTERNATIVE TO***")
print("********************\n")


unique_apps_alternativeto = sum(len(apps) for apps in unique_alternativeto.values())

print("Total number of results (F-DROID): " + str(sum(len(apps) for apps in alternativeto_res.values())))
print("Unique apps (F-DROID): " + str(unique_apps_alternativeto) + "\n")

print("********************")
print("******F-DROID*******")
print("********************\n")

unique_apps_fdroid = sum(len(apps) for apps in unique_fdroid.values())

print("Total number of results (F-DROID): " + str(sum(len(apps) for apps in fdroid_res.values())))
print("Unique apps (F-DROID): " + str(unique_apps_fdroid) + "\n")

print("*******************")
print("***CONSOLIDATION***")
print("*******************\n")

all_merged = {}
for category in keywords.keys():
	all_merged[category] = unique_merged[category].copy()

	#merge fdroid into gps

	for app in unique_fdroid[category]:
		package = app['package']
		packages = list({ each['package'] : each for each in all_merged[category] })
		if package not in packages:
			all_merged[category].append(app)

	#merge alternativeto
	for app in unique_alternativeto[category]:
		package = app['package']
		packages = list({ each['package'] : each for each in all_merged[category] })
		if package not in packages:
			all_merged[category].append(app)


print("Unique apps (ALL): " + str(sum(len(apps) for apps in all_merged.values())) + "\n")

f_serp.close()
f_gps.close()


#####################
#PLOT DISTRIBUTION
#####################

import matplotlib.pyplot as plt

def barPlot(keywords, values, title):
	# SERP API
	fig = plt.figure()
	app_categories = keywords.keys()
	plot_values = [0]*len(app_categories)

	for index,key in enumerate(values.keys()):
		plot_values[index] = len(values[key])

	for i in range(len(app_categories)):
		plt.text(i,plot_values[i],plot_values[i])

	plt.bar(app_categories, plot_values, width = 0.4)
	plt.xlabel("App categories")
	plt.ylabel("#apps")
	plt.title(title)
	plt.show()

barPlot(keywords, unique_serp, title="App distribution (SERP)")
barPlot(keywords, unique_gps, title="App distribution (GPS)")
barPlot(keywords, unique_merged, title="App distribution (GooglePlay [SERP+GPS])")
barPlot(keywords, unique_alternativeto, title = "App distribution (AlternativeTo)")
barPlot(keywords, unique_fdroid, title="App distribution (F-Droid)")
barPlot(keywords, all_merged, title="App distribution (ALL)")