import json

import flask
from flask import Flask, request, current_app

from ScannerService.AppDataScannerService import AppDataScannerService

app = flask.Flask(__name__)
app.config['DEBUG'] = True

app_scanner = AppDataScannerService()


@app.route('/export-data', methods=['POST'])
def give_data():
    try:
        current_app.logger.info('Running export data...')

        #print(request.get_json())
        #app_list = json.loads(request.get_json())
        app_list = request.get_json()

        review_days_old = int(request.args.get('review_days_old'))
        api_consumers = True if request.args.get('api-consumers', default='true') == 'true' else False
        web_scrapers = True if request.args.get('web-scrapers', default='true') == 'true' else False
        return_data = True if request.args.get('return_data', default='false') == 'true' else False

        response = app_scanner.runAppDataScanning(app_list, api_consumers, web_scrapers, review_days_old, return_data)

        # return json.dumps(app_scanner.getAppScannedData())
        return json.dumps(response)
    except Exception as e:
        print("Error processing request:", str(e))
        return {"status": "error", "message": str(e)}, 400


@app.route('/query', methods=['GET'])
def query_app_stores():
    current_app.logger.info('Running query app stores...')

    api = request.args.get('api')
    q = request.args.get('q').split(',')
    apps = request.args.get('apps').split(',')

    current_app.logger.info('Number of keywords (q) = ' + str(len(q)))
    current_app.logger.info('Number of apps (apps) = ' + str(len(apps)))

    return json.dumps(app_scanner.runAppDataQuery(api, q, apps))

@app.route('/query-categories', methods=['GET'])
def query_app_stores_by_category():
    current_app.logger.info('Running query app stores by categories...')

    api = request.args.get('api')

    return json.dumps(app_scanner.runAppDataQueryByCategories(api))


@app.route('/scrap', methods=['GET'])
def scrap_website():
    current_app.logger.info('Scrap website...')

    site = request.args.get('site')
    q = request.args.get('q').split(",")
    apps = request.args.get('apps').split(',')

    current_app.logger.info('Number of keywords (q) = ' + str(len(q)))
    current_app.logger.info('Number of apps (apps) = ' + str(len(apps)))

    return json.dumps(app_scanner.runAppDataQueryScrapper(site, q, apps))


app.run(port=5500, host='0.0.0.0')
