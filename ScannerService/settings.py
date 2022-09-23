# SERP API key
DEFAULT_API_KEY = '****************************************************************'

# MIN REVIEWS
MIN_REVIEWS = 1000


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
               'n_reviews',
               'reviews',
               'similar_apps',
               'package_name',
               'other_apps',
               'play_store_link',
               'features',
               'tags',
               'is_open_source',
               'repository']

prio_serp = [1, 2, 0, 0]
prio_gps = [2, 1, 0, 0]
prio_alt = [0, 0, 1, 0]
prio_fdroid = [0, 0, 0, 1]

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
    'current_version_release_date': prio_gps,
    'version': prio_gps,
    'changelog': prio_gps,
    'n_reviews': prio_gps,
    'reviews': prio_gps,
    'similar_apps': prio_serp,
    'package_name': prio_gps,
    'other_apps': prio_serp,
    'play_store_link': prio_gps,
    'features': prio_alt,
    'tags': prio_alt,
    'is_open_source': prio_alt,
    'repository': prio_fdroid
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
             None,
             'reviews',
             "items",
             None,
             'more_by.items',
             None,
             None,
             None,
             None,
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
            'updated',
            'version',
            'recentChanges',
            'reviews',
            'comments',
            None,
            'appId',
            None,
            'url',
             None,
             None,
             None,
             None]

# keys for the elements to be extracted from AlternativeTo results.
ALT_KEYS = ['app_name',
            'description',
            'summary',
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,               #updated
            None,
            None,
            None,
            None,
            None,               #items 
            'package_name',
            None,               #more-by items
            'url',
            'features',
            'tags',
            'is_open_source',
            None]

# keys for the elements to be extracted from FDroid results.
FDROID_KEYS = ['app_name',
            'description',
            'summary',
            None,
            None,
            None,
            None,
            'developer',
            'developer_site',
            None,
            'current_version_release_date',               #updated
            'version',
            'changelog',
            None,
            None,
            None,               #items 
            'package_name',
            None,               #more-by items
            'url',
            None,
            None,
            'is_open_source',
            'repository']

INFO_MATRIX = [GPS_KEYS, SERP_KEYS, ALT_KEYS, FDROID_KEYS]
