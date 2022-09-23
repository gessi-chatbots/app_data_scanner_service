import os, json

found_apps = []
all_apps = []
missing_apps = []
not_missing_apps = []
with open("/home/quim-motger/Projects/PhD/app_data_scanner_service/scripts/apps.json") as f1:
    found_apps = json.load(f1)

    # all_matches = 0
    # for app in found_apps:
    #     match = 0
    #     for i in range(0, len(found_apps)):
    #         if app['package_name'] == found_apps[i]['package_name']:
    #             match += 1
    #             all_matches += 1
    #     if match > 1:
    #         print("!!!!!!!!!!!!!!!!!!! This app is more than once: " + app['package_name'])
    # print(all_matches)

    with open("/home/quim-motger/Projects/PhD/app_data_scanner_service/data/app_query_MERGED.json") as f2:
        all_apps = json.load(f2)

        

        #check
        for app1 in all_apps:
            found = False
            for app2 in found_apps:
                if app1['package'] == app2['package_name']:
                    found = True
            if found == False:
                missing_apps.append(app1)
            else:
                not_missing_apps.append(app1)


with open('missing-apps.json', 'w') as outfile:
   json.dump(missing_apps, outfile)
   print("Missing apps: "+ str(len(missing_apps)))
   print("Found apps: " + str(len(found_apps)))
   print("Not missing apps: " + str(len(not_missing_apps)))
   print("All apps: " + str(len(all_apps)))