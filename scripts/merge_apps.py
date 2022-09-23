import os, json

apps = []
for filename in os.listdir("/home/quim-motger/Projects/PhD/app_data_scanner_service/data/scanApps/3rd-round"):
   with open(os.path.join("/home/quim-motger/Projects/PhD/app_data_scanner_service/data/scanApps/3rd-round", filename), 'r') as f: # open in readonly mode
      data = json.load(f)
      apps += data

non_duplicate_apps = []

for i in range(0, len(apps)):
   found = False
   for j in range(0, len(apps)):
      if i != j and i > j and apps[i]['package_name'] == apps[j]['package_name']:
         found = True
   if not found:
      non_duplicate_apps.append(apps[i])

print("Total number of apps: " + str(len(non_duplicate_apps)))
with open("/home/quim-motger/Projects/PhD/app_data_scanner_service/data/scanApps/merged-apps.json", 'w') as outfile:
   json.dump(non_duplicate_apps, outfile)