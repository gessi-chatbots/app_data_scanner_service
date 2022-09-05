import json

import flask
from flask import Flask, request, current_app

from ScannerService.AppDataScannerService import AppDataScannerService

app = flask.Flask(__name__)
app.config['DEBUG'] = True

app_scanner = AppDataScannerService()

@app.route('/export-data', methods=['POST'])
def give_data():

    current_app.logger.info('Running export data...')

    app_list = json.loads(request.get_json())

    api_consumers = True if request.args.get('api-consumers', default='true') == 'true' else False
    web_scrapers = True if request.args.get('web-scrapers', default='true') == 'true' else False

    response = app_scanner.runAppDataScanning(app_list, api_consumers, web_scrapers)

    #return json.dumps(app_scanner.getAppScannedData())
    return json.dumps(response)

@app.route('/query', methods=['GET'])
def query_app_stores():

    current_app.logger.info('Running query app stores...')

    api = request.args.get('api')
    q = request.args.get('q').split(',')
    apps = request.args.get('apps').split(',')

    current_app.logger.info('Number of keywords (q) = ' + str(len(q)))
    current_app.logger.info('Number of apps (apps) = ' + str(len(apps)))

    return json.dumps(app_scanner.runAppDataQuery(api, q, apps))

@app.route('/scrap', methods=['GET'])
def scrap_website():

    current_app.logger.info('Scrap website...')

    site = request.args.get('site')
    q = request.args.get('q').split(",")
    apps = request.args.get('apps').split(',')

    current_app.logger.info('Number of keywords (q) = ' + str(len(q)))
    current_app.logger.info('Number of apps (apps) = ' + str(len(apps)))

    return json.dumps(app_scanner.runAppDataQueryScrapper(site, q, apps))

app.run()
