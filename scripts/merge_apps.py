import os, json

apps = []
for filename in os.listdir("data/scanApps"):
   if 'fail' not in filename:
      with open(os.path.join("data/scanApps", filename), 'r', encoding="utf8") as f: # open in readonly mode
         data = json.load(f)
         apps += data

non_duplicate_apps = []

for i in range(0, len(apps)):
   found = False
   for j in range(0, len(apps)):
      if i != j and i > j and apps[i]['package_name'] == apps[j]['package_name']:
      #if i != j and i > j and apps[i]['package'] == apps[j]['package']:
         found = True
   if not found:
      non_duplicate_apps.append(apps[i])

print("Total number of apps: " + str(len(non_duplicate_apps)))
with open("data/MApp-KG-v2.json", 'w') as outfile:
   json.dump(non_duplicate_apps, outfile)