from google_play_scraper import app, reviews, search

from ScannerService.IDataRetriever import IDataRetriever

from flask import current_app

import time

class GPSService(IDataRetriever):

    def __init__(self, review_number=200, review_lang='en'):
        self._review_number = review_number
        self._review_lang = review_lang

    def get_data(self, app_name: str):
        try:
            result = app(app_name)

            #paginate reviews TODO
            count = 0 if result['reviews'] is None else result['reviews']

            #limit if too much
            count = 1000 if count > 1000 else count

            i = 0
            comment_list_aux = []
            token = None

            while i < count:
                comments, token = reviews(app_name, count=100, lang=self._review_lang, continuation_token=token)
                #time.sleep(3)
                i += len(comments)
                comment_list_aux += comments

            #print("We found " + str(len(comment_list_aux)))
            #print(comment_list_aux[0])

            comment_list = []
            for comment in comment_list_aux:
                aux = {'reviewId': comment['reviewId'], 'review': comment['content'], 
                'reply': comment['replyContent'], 'userName': comment['userName'], 
                'score': comment['score'], 'source': 'Google Play'}
                comment_list.append(aux)
            result['comments'] = comment_list

            #print(result)
            
            return result
        except Exception as e: 
            print(e)
            print("There was a network error during " + app_name + ". Data might not be complete")
            #current_app.logger.error("App " + app_name + " could not be extracted from GPS")

    def queryAppData(self, q):
        current_app.logger.info('Querying ' + q + ' from GPS')
        result = search(q)
        return result