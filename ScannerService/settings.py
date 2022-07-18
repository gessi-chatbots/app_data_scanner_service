# SERP API key
DEFAULT_API_KEY = 'a0772ea82034c90f541eb8c5d9a6281f18a39a82737a6ea84d01c5ba4b830ac5'


# list of info to be extracted. These are the keys for the info that the service returns.
# When adding a new API, the list of keys should follow the same order has here, with "None" if the API doesn't provide
# a piece of data
NEEDED_INFO = ['app_name',
               'description',
               'summary',
               'category',
               'categoryId',
               'in_app_purchases',
               'android_version',
               'developer',
               'developer_site',
               'release_date',
               'current_version_release_date',
               'version',
               'changelog',
               'reviews',
               'similar_apps',
               'package_name',
               'other_apps',
               'play_store_link']

prio_gps = [0, 1]
prio_serp = [1, 0]

# list of priorities for extracting data. The service will try to retrieve the data from the highest priority source.
# If it cannot find it, then it will try the following until info is retrieved or until the end.
PRIORITY_LIST = {
    'app_name': prio_gps,
    'description': prio_gps,
    'summary': prio_gps,
    'category': prio_gps,
    'categoryId': prio_gps,
    'in_app_purchases': prio_serp,
    'android_version': prio_gps,
    'developer': prio_gps,
    'developer_site': prio_gps,
    'release_date': prio_gps,
    'current_version_release_date': prio_serp,
    'version': prio_gps,
    'changelog': prio_gps,
    'reviews': prio_gps,
    'similar_apps': prio_serp,
    'package_name': prio_gps,
    'other_apps': prio_serp,
    'play_store_link': prio_gps

}

# keys for the elements to be extracted from SERP API results.
# Note that the raw results get flattened to ease data extraction
SERP_KEYS = ['product_info.title',
             'product_info.description',
             None,
             'product_info.categories',
             None,
             "product_info.extansions",
             None,
             'product_info.authors',
             'additional_information.developer',
             None,
             "additional_information.updated",
             'additional_information.current_version',
             'what_s_new.snippet',
             'reviews',
             "items",
             None,
             'more_by.items',
             None]

# keys for the elements to be extracted from GPS API results.
GPS_KEYS = ['title',
            'description',
            'summary',
            'genre',
            'genreId',
            'offersIAP',
            'androidVersion',
            'developer',
            'developerWebsite',
            'released',
            None,
            'version',
            'recentChanges',
            'comments',
            None,
            'appId',
            None,
            'url']

INFO_MATRIX = [GPS_KEYS, SERP_KEYS]
