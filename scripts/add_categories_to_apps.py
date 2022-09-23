import json

with open("/home/quim-motger/Projects/PhD/app_data_scanner_service/data/scanApps/merged-apps.json") as f1:
    apps = json.load(f1)

    with open("/home/quim-motger/Projects/PhD/app_data_scanner_service/data/apps_by_category.json") as f2:
        categories = json.load(f2)

        for app in apps:
            app['categories'] = []

            for category in categories.keys():
                found = False
                for cat_app in categories[category]:
                    if app['package_name'] == cat_app['package']:
                        found = True
                if found:
                    app['categories'].append(category)

            print("App " + app['package_name'] + " has: " + str(app['categories']))

        with open("/home/quim-motger/Projects/PhD/app_data_scanner_service/data/scanApps/merged-apps-with-categories.json", 'w') as outfile:
            json.dump(apps, outfile)