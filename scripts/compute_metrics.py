import json
import matplotlib.pyplot as plt

with open("/home/quim-motger/Projects/PhD/app_data_scanner_service/data/scanApps/2nd-round/merged-apps-reviews-with-date-filter.json") as f1:
    apps = json.load(f1)
   
    n_reviews = []
    out = 0

    sum = 0
    apps_with_more_than_zero = []
    apps_with_min_ten = []
    apps_with_min_fifty = []
    apps_with_min_hundred = []
    apps_with_min_thousand = []

    with_at_least_one_reviews = 0
    with_at_least_ten_reviews = 0
    with_at_least_fifty_reviews = 0
    with_at_least_hundred_reviews = 0
    with_at_least_thousand_reviews = 0

    for app in apps:
        # if app['n_reviews'] is not None:
        #     sum += int(app['n_reviews'])
        # if app['reviews'] is not None:
        #     sum_act += int(len(app['reviews']))
        if app['reviews'] is not None:
            x = len(app['reviews'])
            sum += x
            n_reviews.append(x)
            if x > 0:
                apps_with_more_than_zero.append(app)
                with_at_least_one_reviews += len(app['reviews'])
            if x >= 10:
                apps_with_min_ten.append(app)
                with_at_least_ten_reviews += len(app['reviews'])
            if x>= 50:
                apps_with_min_fifty.append(app)
                with_at_least_fifty_reviews += len(app['reviews'])
            if x >= 100:
                apps_with_min_hundred.append(app)
                with_at_least_hundred_reviews += len(app['reviews'])
            if x >= 1000:
                apps_with_min_thousand.append(app)
                with_at_least_thousand_reviews += len(app['reviews'])
            if x > 100000:
                print(app['package_name'])

    print(sum)
    print(sorted(n_reviews))
    print(len(apps))
    print("With at least 1 review: " + str(len(apps_with_more_than_zero)))
    print("With at least 10 review: " + str(len(apps_with_min_ten)))
    print("With at least 50 review: " + str(len(apps_with_min_fifty)))
    print("With at least 100 review: " + str(len(apps_with_min_hundred)))
    print("With at least 1000 review: " + str(len(apps_with_min_thousand)))

    with_at_least_one = [0]*10
    with_at_least_ten = [0]*10
    with_at_least_fifty = [0]*10
    with_at_least_hundred = [0]*10
    with_at_least_thousand = [0]*10

    with open("/home/quim-motger/Projects/PhD/app_data_scanner_service/data/apps_by_category.json") as f2:
        apps_by_category = json.load(f2)        

        #with-one
        for app in apps_with_more_than_zero:
            i = 0
            for key in apps_by_category.keys():
                #todo
                found = False
                for app2 in apps_by_category[key]:
                    if app['package_name'] == app2['package']:
                        found = True
                if found:
                    with_at_least_one[i] += 1
                i += 1

        #with-ten
        for app in apps_with_min_ten:
            i = 0
            for key in apps_by_category.keys():
                #todo
                found = False
                for app2 in apps_by_category[key]:
                    if app['package_name'] == app2['package']:
                        found = True
                if found:
                    with_at_least_ten[i] += 1
                i += 1

         #with-ten
        for app in apps_with_min_fifty:
            i = 0
            for key in apps_by_category.keys():
                #todo
                found = False
                for app2 in apps_by_category[key]:
                    if app['package_name'] == app2['package']:
                        found = True
                if found:
                    with_at_least_fifty[i] += 1
                i += 1

        #with-hundred
        for app in apps_with_min_hundred:
            i = 0
            for key in apps_by_category.keys():
                #todo
                found = False
                for app2 in apps_by_category[key]:
                    if app['package_name'] == app2['package']:
                        found = True
                if found:
                    with_at_least_hundred[i] += 1
                i += 1

        #with-thousand
        for app in apps_with_min_thousand:
            i = 0
            for key in apps_by_category.keys():
                #todo
                found = False
                for app2 in apps_by_category[key]:
                    if app['package_name'] == app2['package']:
                        found = True
                if found:
                    with_at_least_thousand[i] += 1
                i += 1

    #print(sum_act)
    print(with_at_least_one)
    print(with_at_least_ten)
    print(with_at_least_fifty)
    print(with_at_least_hundred)
    print(with_at_least_thousand)

    print(with_at_least_one_reviews)
    print(with_at_least_ten_reviews)
    print(with_at_least_fifty_reviews)
    print(with_at_least_hundred_reviews)
    print(with_at_least_thousand_reviews)


    # we store what we want
    # first, we limit max reviews to 9,999
    for app in apps_with_min_fifty:
        if len(app['reviews']) >= 10000:
            app['reviews'] = app['reviews'][0:9999]
        print(len(app['reviews']))

    with open("/home/quim-motger/Projects/PhD/app_data_scanner_service/data/scanApps/merged-apps.json", 'w') as outfile:
        json.dump(apps_with_min_fifty, outfile)