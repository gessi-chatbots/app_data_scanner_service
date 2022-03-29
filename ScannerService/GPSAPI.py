import utils
from ScannerService.APIScanner import APIScanner
from google_play_scraper import app, reviews
from google_play_scraper.exceptions import NotFoundError


class GPSAPI(APIScanner):

    def __init__(self, info):
        super().__init__()
        self.keys = info

    def scanAppData(self, app_list, include_reviews=True, review_number=50):
        app_info_list = []
        for package in app_list:
            result = app(package)
            trimmed_info = self.extract_info(result, relevant_keys=self.keys)
            if include_reviews:
                comments, cont = reviews(package, count=review_number)
                comment_list = []
                for comment in comments:
                    auxiliar_dict = {'review': comment['content'], 'reply': comment['replyContent']}
                    comment_list.append(auxiliar_dict)
                trimmed_info['reviews'] = comment_list
            app_info_list.append(trimmed_info)
        return app_info_list

    @staticmethod
    def extract_info(dict, relevant_keys):
        result = {}
        for key in relevant_keys:
            result[key] = dict[key]
        return result
