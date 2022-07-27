from google_play_scraper import app, reviews, search

from ScannerService.IDataRetriever import IDataRetriever

from flask import current_app


class GPSService(IDataRetriever):

    def __init__(self, review_number=200, review_lang='en'):
        self._review_number = review_number
        self._review_lang = review_lang

    def get_data(self, app_name: str):
        try:
            result = app(app_name)

            #paginate reviews TODO
            comments, cont = reviews(app_name, count=result['reviews'], lang=self._review_lang)

            comment_list = []
            for comment in comments:
                aux = {'reviewId': comment['reviewId'], 'review': comment['content'], 
                'reply': comment['replyContent'], 'userName': comment['userName'], 
                'score': comment['score'], 'source': 'Google Play'}
                comment_list.append(aux)
            result['comments'] = comment_list
            return result
        except Exception as e: 
            #print(e)
            current_app.logger.error("Error. App " + app_name + " could not be extracted from GPS")

    def queryAppData(self, q):
        current_app.logger.info('Querying ' + q + ' from GPS')
        result = search(q)
        return result