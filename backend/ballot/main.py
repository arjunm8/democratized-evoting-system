#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:06:59 2020

@author: arjun
"""

import logging
# Imports the Google Cloud client library

from flask import Flask, request
from models import db, Ballot,Candidate, User
import json
import traceback
import requests

blockchain_service_url = "http://0.0.0.0:5006/blockchain/vote"
notification_service_url = "http://0.0.0.0:5005/notification"
ballot_service_url = "http://192.168.0.102:5003"


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/evdb"

db.init_app(app)

with app.app_context():
    db.create_all()



@app.route('/ballot', methods=["POST"])
def vote():
    '''
    create a new poll.
    callers: all users
    '''
    data = request.form.to_dict()
    ballot = Ballot()
    try:
        payload = {'candidate_id': data["candidate_id"]}
        response = requests.request("POST", blockchain_service_url, data = payload)
        data["transaction_id"] = json.loads(response.text)["receipt"]
        ballot.deserialize(json=data)
        ballot.save()
        response_object = ballot.serialize()

        try:
            payload = {
                    'number': User.query.filter(
                            User.id==response_object["user_id"]
                            ).first().phone,
                    'link': ballot_service_url+"/"+str(response_object["id"])
                    }
            
            requests.request("POST", notification_service_url, data = payload)
        except:
            traceback.print_exc()
            pass
        
        return json.dumps(response_object),200
    except Exception as e:
        traceback.print_exc()
        return str(e),500


@app.route('/ballot/<int:id>', methods=["GET"])
def get_ballot_object(id):
    '''
    get ballot object by id
    callers: system
    '''
    ballot = Ballot.query.filter(Ballot.id == id).first()
    if ballot:
        ballot = ballot.serialize()
        return json.dumps(ballot)
    else:
        return "",404


@app.route('/<int:id>', methods=["GET"])
def short_get_ballot_object(id):
    '''
    get ballot object by id
    callers: system
    '''
    ballot = Ballot.query.filter(Ballot.id == id).first()
    if ballot:
        ballot = ballot.serialize()
        return json.dumps(ballot)
    else:
        return "",404


@app.route('/candidates', methods=["GET"])
def list_constituencies():
    '''
    list available constituencies
    callers: all users
    '''
    candidates = Candidate.query.all()

    if candidates:
        candidate_list = [candidate.serialize() for candidate in candidates]

        return json.dumps(candidate_list)
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
    app.run(debug=True,host="0.0.0.0",port=5003)
