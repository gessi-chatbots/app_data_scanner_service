import json

import flask
import werkzeug
from flask import Flask, request
from werkzeug.exceptions import abort
import time
import logging

from ServiceController.AppDataScannerService import AppDataScannerService

# log_file = open("log.info", 'w', encoding='utf-8')
logging.basicConfig(filename="log.info", level=logging.DEBUG)
app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'Bad request', 400


@app.route('/export-data', methods=['POST'])
def give_data():
    initial_time = time.perf_counter()
    data = []
    if request.method == 'POST':
        data = json.loads(request.data)
    app_list = []
    app_names = []
    for app_info in data:
        try:
            app_list.append(app_info['package_name'])
        except KeyError:
            pass
        try:
            app_names.append(app_info['app_name'])
        except KeyError:
            pass

    app_scanner = AppDataScannerService()
    app_scanner.runAppDataScanning(app_list, app_names)
    final_time = time.perf_counter()
    total_time = final_time-initial_time
    logging.debug(f'"Request total time: {total_time} s')
    return json.dumps(app_scanner.getAppScannedData())


app.run()
