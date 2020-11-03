#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:06:59 2020

@author: arjun
"""

import logging
# Imports the Google Cloud client library

from flask import Flask, request
import traceback
import requests



app = Flask(__name__)


@app.route('/notification', methods=["POST"])
def send_notifcation():
    '''
    send verification link sms
    callers: system
    '''
    headers = {
        'authorization': 'tFm8yNZaPgfJRp26AwBeKhuLQVYHrvx9DTOzCj4GcWnXES7kibDvYeraGq4JxLEVC29lo3gKTkSAhRNj',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
    }
    data = {
      'sender_id': 'FSTSMS',
      'language': 'english',
      'route': 'qt',
      'numbers': "",
      'message': '39131',
      'variables': '{#FF#}',
    }
    try:
        data['numbers'] = request.form.get("number")[3:]
        data['variables_values'] = request.form.get("link")
        print(data)
        response = requests.post('https://www.fast2sms.com/dev/bulk', headers=headers, data=data)
        if response.status_code == 200:
            return "",200
        else:
            return "failed to send", 500
    except Exception as e:
        traceback.print_exc()
        return str(e),500


@app.route('/')
def hello():
    return 'Notification Service is active'


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]


if __name__ =="__main__":
    app.run(debug=True,port=5005)
