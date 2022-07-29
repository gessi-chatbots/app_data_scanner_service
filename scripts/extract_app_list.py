import json

import csv

def unique_apps(set):
	apps = []
	for category in set.keys():
		for app in set[category]:
			new_package = app['package']
			old_packages = list({ each : each for each in apps })
			if new_package not in old_packages:
				apps.append(app['package'])
	return apps

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
	for i in range(0, len(data_serp[key])):
		if 'organic_results' in data_serp[key][i].keys():
			for results in data_serp[key][i]['organic_results']:
				#We ignore 'Similar apps' -- WHY??????
				if 'title' not in results or results['title'] == 'More results' or results['title'] == 'Similar apps':
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
unique_googleplay = {}
unique_fdroid = {}
unique_alternativeto = {}

for category in keywords.keys():
	unique_serp[category] = list({ each['package'] : each for each in serp_res[category] }.values())
	unique_gps[category] = list({ each['package'] : each for each in gps_res[category] }.values())
	unique_fdroid[category] = list({ each['package'] : each for each in fdroid_res[category] }.values())
	unique_alternativeto[category] = list({ each['package'] : each for each in alternativeto_res[category] }.values())

	unique_googleplay[category] = unique_gps[category].copy()
	for app in unique_serp[category]:
		package = app['package']
		packages = list({ each['package'] : each for each in gps_res[category] })
		if package not in packages:
			unique_googleplay[category].append(app)

all_merged = {}
for category in keywords.keys():
	all_merged[category] = unique_googleplay[category].copy()

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

serp_count = sum(len(apps) for apps in serp_res.values())
unique_serp_count = sum(len(apps) for apps in unique_serp.values())
unique_serp_count_wo_duplicates = len(unique_apps(unique_serp))

gps_count  = sum(len(apps) for apps in gps_res.values())
unique_gps_count = sum(len(apps) for apps in unique_gps.values())
unique_gps_count_wo_duplicates = len(unique_apps(unique_gps))

unique_googleplay_count = sum(len(apps) for apps in unique_googleplay.values())
unique_googleplay_count_wo_duplicates = len(unique_apps(unique_googleplay))

alternativeto_count = sum(len(apps) for apps in alternativeto_res.values())
unique_alternativeto_count = sum(len(apps) for apps in unique_alternativeto.values())
unique_alternativeto_count_wo_duplicates = len(unique_apps(unique_alternativeto))

fdroid_count = sum(len(apps) for apps in fdroid_res.values())
unique_fdroid_count = sum(len(apps) for apps in unique_fdroid.values())
unique_fdroid_count_wo_duplicates = len(unique_apps(unique_fdroid))

all_apps = unique_apps(all_merged)
unique_all_apps_count = sum(len(apps) for apps in all_merged.values())
unique_all_apps_count_wo_duplicates = len(all_apps)

print("Data Source\t\t#results\t#results-without-duplicates-in-category\t#results-without-duplicates")
print("SERP\t\t\t" + str(serp_count) + "\t\t" + str(unique_serp_count) + "\t\t\t\t\t" + str(unique_serp_count_wo_duplicates))
print("GPS\t\t\t" + str(gps_count) + "\t\t" + str(unique_gps_count) + "\t\t\t\t\t" + str(unique_gps_count_wo_duplicates))
print("GooglePlay(SERP+GPS)\t" + str(serp_count+gps_count) + "\t\t" + str(unique_googleplay_count) + "\t\t\t\t\t" + str(unique_googleplay_count_wo_duplicates))
print("Alternative-To\t\t" + str(alternativeto_count) + "\t\t" + str(unique_alternativeto_count) + "\t\t\t\t\t" + str(unique_alternativeto_count_wo_duplicates))
print("F-Droid\t\t\t" + str(fdroid_count) + "\t\t" + str(unique_fdroid_count) + "\t\t\t\t\t" + str(unique_fdroid_count_wo_duplicates))
print("ALL\t\t\t" + str(serp_count) + "\t\t" + str(unique_serp_count) + "\t\t\t\t\t" + str(unique_serp_count_wo_duplicates) + "\n")




####################
# INTERSECTION
####################

#TO-DO


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

# barPlot(keywords, unique_serp, title="App distribution (SERP)")
# barPlot(keywords, unique_gps, title="App distribution (GPS)")
# barPlot(keywords, unique_googleplay, title="App distribution (GooglePlay [SERP+GPS])")
# barPlot(keywords, unique_alternativeto, title = "App distribution (AlternativeTo)")
# barPlot(keywords, unique_fdroid, title="App distribution (F-Droid)")
# barPlot(keywords, all_merged, title="App distribution (ALL)")

print('**********************')
print('***INTERSECTION*******')
print('**********************')

serp_list = unique_apps(unique_serp)
gps_list = unique_apps(unique_gps)
googleplay_list = unique_apps(unique_googleplay)
fdroid_list = unique_apps(unique_fdroid)
alternativeto_list = unique_apps(unique_alternativeto)


#TODO - intersect all into a unique JSON array
all_apps = []
for category in all_merged.keys():
	for app in all_merged[category]:
		new_package = app['package']
		old_packages = list({ each['package'] : each for each in all_apps })
		if new_package not in old_packages:
			all_apps.append(app)
#print(all_apps)
###


# INTERSECT 1: SERP + GPS
serp_not_gps = 0
gps_not_serp = 0
serp_and_gps = 0
for app in serp_list:
	if app in gps_list:
		serp_and_gps += 1
	else:
		serp_not_gps += 1
for app in gps_list:
	if app not in serp_list:
		gps_not_serp += 1

#print("Intersection = " + str(serp_and_gps) + ". Only GPS = " + str(gps_not_serp) + ". Only SERP = " + str(serp_not_gps))

#INTERSECT 2: GP + AT + FDROID

gp_only = []
at_only = []
fdroid_only = []

gp_at_only = []
gp_fdroid_only = []
at_fdroid_only = []

gp_at_frdoid = []

for app in googleplay_list:
	if app not in fdroid_list and app not in alternativeto_list:
		gp_only.append(app)
	elif app not in fdroid_list and app in alternativeto_list:
		gp_at_only.append(app)
	elif app in fdroid_list and app not in alternativeto_list:
		gp_fdroid_only.append(app)
	elif app in fdroid_list and app in alternativeto_list:
		gp_at_frdoid.append(app)

for app in alternativeto_list:
	if app not in googleplay_list and app not in fdroid_list:
		at_only.append(app)
	elif app not in googleplay_list and app in fdroid_list:
		at_fdroid_only.append(app)

for app in fdroid_list:
	if app not in googleplay_list and app not in alternativeto_list:
		fdroid_only.append(app)

# print("Only Google Play = " + str(len(gp_only)) + ". Only AlternativeTo = " + str(len(at_only)) + ". Only FDroid = " + str(len(fdroid_only)))
# print("Google Play and Alternative To = " + str(len(gp_at_only)) + ". Google Play and F-Droid = " + str(len(gp_fdroid_only)) + ". AlternativeTo and F-Droid only = " + str(len(at_fdroid_only)))
# print("Google Play, AlternativeTo and F-Droid = " + str(len(gp_at_frdoid)))

# print("Google Play and AlternativeTo: " + str(gp_at_only))
# print("Google Play and FDroid: " + str(gp_fdroid_only))
# print("AlternativeTo and FDroid: " + str(at_fdroid_only))

# print(gp_at_frdoid)
