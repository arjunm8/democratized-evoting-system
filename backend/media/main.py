#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:06:59 2020

@author: arjun
"""

import logging
# Imports the Google Cloud client library
from time import time
from flask import Flask, request, send_file
import os,json
import traceback



app = Flask(__name__)

@app.route('/media', methods=["POST"])
def upload_file():
    '''
    upload a file to get a direct url
    callers: all users
    '''
    uploaded_file = request.files.get('file')
    if uploaded_file:
        filename = (str(int(time()))+"_"+uploaded_file.filename)

        uploaded_file.save(os.path.join('storage/', filename))

        url = request.url+"/"+filename

        return json.dumps({"url":url}),200
    else:
        return "",500


@app.route('/media/<string:filename>', methods=["GET"])
def download_file(filename):
    '''
    download a file
    callers: all users
    '''
    download_file = os.path.join('storage/',filename)

    if os.path.exists(download_file):
        return send_file(download_file, as_attachment=True),200
    else:
        return "file not found",404



@app.route('/')
def hello():
    return 'Media Service is active'


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]


if __name__ =="__main__":
    app.run(debug=True,port=5002)
