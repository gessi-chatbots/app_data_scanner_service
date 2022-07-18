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

    app_list = []
    app_names = []
    if request.method == 'POST':
        app_list = json.loads(request.form['app_list'])
        app_names = json.loads(request.form['app_names'])
    app_scanner.runAppDataScanning(app_list, app_names)
    return json.dumps(app_scanner.getAppScannedData())

@app.route('/query', methods=['GET'])
def query_app_stores():

    current_app.logger.info('Running query app stores...')

    api = request.args.get('api')
    q = request.args.get('q').split(',')

    current_app.logger.info('Number of keywords (q) = ' + str(len(q)))
    current_app.logger.info(q[0])

    return json.dumps(app_scanner.runAppDataQuery(api, q))

@app.route('/scrap', methods=['GET'])
def scrap_website():

    current_app.logger.info('Scrap website...')

    site = request.args.get('site')
    q = request.args.get('q').split(",")

    return json.dumps(app_scanner.runAppDataQueryScrapper(site, q))

app.run()
