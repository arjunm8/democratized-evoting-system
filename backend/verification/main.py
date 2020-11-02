#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:06:59 2020

@author: arjun
"""

import logging
# Imports the Google Cloud client library

from flask import Flask, request
from models import db, Document
import json
import traceback



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/evdb"

db.init_app(app)

with app.app_context():
    db.create_all()


def is_legit(user_id,kind,number,image_url):
    '''
    @TODO connect with govt. doc verification api eg. uidai/aadhar
    '''
    return "",True


@app.route('/verification/document', methods=["POST"])
def post_document():
    '''
    post a document for verification
    callers: all users
    '''
    data = request.form.to_dict()

    try:
        err,verified = is_legit(**data)
        if verified:
            document = Document()
            document.deserialize(json=data)
            document.save()
            return json.dumps(document.serialize()),200
        else:
            return err,422

    except Exception as e:
        traceback.print_exc()
        return str(e),500


@app.route('/verification/user/<int:user_id>', methods=["GET"])
def get_doc_by_user(user_id):
    '''
    Check if a user has a verified doc in the db
    callers: all users
    '''
    document = Document.query.filter(Document.user_id == user_id).first()
    if document:
        return json.dumps(document.serialize()),200
    else:
        return "not found",404


@app.route('/verification/user/<int:user_id>', methods=["DELETE"])
def delete_doc_by_user(user_id):
    '''
    delete document by user id.
    callers: all users
    '''
    document = Document.query.filter(Document.user_id == user_id).first()
    if document:
        document.delete()
        return "",204
    else:
        return "",404


@app.route('/')
def hello():
    return 'Verification Service is active'


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]


if __name__ =="__main__":
    app.run(debug=True,port=5001)
