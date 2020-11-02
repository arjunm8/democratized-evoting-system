#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:06:59 2020

@author: arjun
"""

import logging
# Imports the Google Cloud client library

from flask import Flask, request
from models import db, Ballot
import json
import traceback



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/evdb"

db.init_app(app)

with app.app_context():
    db.create_all()



@app.route('/ballot', methods=["POST"])
def create_user():
    '''
    create a new poll.
    callers: all users
    '''
    data = request.form.to_dict()
    ballot = Ballot()
    try:
        ballot.deserialize(json=data)
        ballot.save()
        return json.dumps(ballot.serialize()),200
    except Exception as e:
        traceback.print_exc()
        return str(e),500


@app.route('/ballot/<int:id>', methods=["GET"])
def get_user(id):
    '''
    get ballot object by id
    callers: all users
    '''
    ballot = Ballot.query.filter(Ballot.id == id).first()
    if ballot:
        ballot = ballot.serialize()
        return json.dumps(ballot)
    else:
        return "",404



@app.route('/')
def hello():
    return 'Ballot Service is active'


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]


if __name__ =="__main__":
    app.run(debug=True,port=5003)