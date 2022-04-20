import json

import flask
from flask import Flask, request

from ScannerService.AppDataScannerService import AppDataScannerService

app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route('/export-data', methods=['POST'])
def give_data():
    app_list = []
    app_names = []
    if request.method == 'POST':
        app_list = json.loads(request.form['app_list'])
        app_names = json.loads(request.form['app_names'])
    app_scanner = AppDataScannerService()
    app_scanner.runAppDataScanning(app_list, app_names)
    return json.dumps(app_scanner.getAppScannedData())


app.run()
