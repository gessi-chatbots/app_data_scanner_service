from google_play_scraper import app, reviews

from ScannerService.IDataRetriever import IDataRetriever


class GPSService(IDataRetriever):

    def __init__(self, review_number=50):
        self._review_number = review_number

    def get_data(self, app_name: str):
        result = app(app_name)
        comments, cont = reviews(app_name, count=self._review_number)
        comment_list = []
        for comment in comments:
            aux = {'review': comment['content'], 'reply': comment['replyContent']}
            comment_list.append(aux)
        result['comments'] = comment_list
        return result

