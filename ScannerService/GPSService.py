from google_play_scraper import app, reviews, search

from ScannerService.IDataRetriever import IDataRetriever

from flask import current_app

from ScannerService.Utils import Utils

import datetime

from ScannerService.settings import MIN_REVIEWS

class GPSService(IDataRetriever):

    def __init__(self, review_number=200, review_lang='en'):
        self._review_number = review_number
        self._review_lang = review_lang

    def get_data(self, app_name: str):
        comment_list_aux = []
        comment_list = []
        try:
            result = app(app_name)
            
            millis = datetime.datetime.fromtimestamp(result['updated']*1000 / 1e3)
            result['updated'] = Utils.millis_to_timestamp(millis)

            # #paginate reviews TODO
            # count = 0 if result['reviews'] is None else result['reviews']

            # #limit if too much
            # count = 1000 if count > 1000 else count

            token = None
            last_review = datetime.datetime.now()
            one_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

            comments, token = reviews(app_name, count=200, lang=self._review_lang, continuation_token=token)
            comment_list_aux += comments
            last_review = comments[len(comments) - 1]['at']

            while token is not None:
            #while token is not None and last_review > one_year_ago:
                comments, token = reviews(app_name, count=200, lang=self._review_lang, continuation_token=token)
                comment_list_aux += comments
                last_review = comments[len(comments) - 1]['at']

            for comment in comment_list_aux:
                # if millis <= comment['at']:
                aux = {'reviewId': comment['reviewId'], 'review': comment['content'], 
                'reply': comment['replyContent'], 'userName': comment['userName'], 
                'score': comment['score'], 'at': Utils.millis_to_timestamp(comment['at'])}
                comment_list.append(aux)
            result['comments'] = comment_list

            #print(result)
            
            return result
        except Exception as e: 
            print(e)
            print("There was a network error during " + app_name + ". Data might not be complete")
            comment_list = []
            for comment in comment_list_aux:
                # if millis <= comment['at']:
                aux = {'reviewId': comment['reviewId'], 'review': comment['content'], 
                'reply': comment['replyContent'], 'userName': comment['userName'], 
                'score': comment['score'], 'at': Utils.millis_to_timestamp(comment['at'])}
                comment_list.append(aux)
            result['comments'] = comment_list            
            return result
            #current_app.logger.error("App " + app_name + " could not be extracted from GPS")

    def queryAppData(self, q):
        current_app.logger.info('Querying ' + q + ' from GPS')
        result = search(q)
        return result