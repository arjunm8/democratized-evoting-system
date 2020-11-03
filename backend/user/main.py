#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:06:59 2020

@author: arjun
"""

import logging
# Imports the Google Cloud client library

from flask import Flask, request
from models import db, User, Constituency
import json
import traceback



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/evdb"

db.init_app(app)

with app.app_context():
    db.create_all()



@app.route('/user', methods=["GET"])
def check_user():
    '''
    get user object by email/phone
    callers: all users
    '''
    #@TODO replace by firebase id token verification
    phone = request.args.get("phone")
    user = User.query.filter(User.phone == phone).first()
    if user:
        user = user.serialize()
        return json.dumps(user)
    else:
        return "",404


@app.route('/user/<int:id>', methods=["GET"])
def get_user(id):
    '''
    get user object by id
    callers: all users
    '''
    user = User.query.filter(User.id == id).first()
    if user:
        user = user.serialize()
        return json.dumps(user)
    else:
        return "",404

@app.route('/user', methods=["POST"])
def create_user():
    '''
    create a new user.
    callers: all users
    '''
    data = request.form.to_dict()
    user = User()
    user.deserialize(json=data)
    try:
        user.save()
        return json.dumps(user.serialize()),200
    except Exception as e:
        traceback.print_exc()
        return str(e),500


@app.route('/user/<int:id>', methods=["PATCH"])
def update_user(id):
    '''
    update a user record by id.
    callers: all users
    '''
    data = request.args.to_dict()
    user = User.query.filter(User.id == id).first()

    user.deserialize(json=data)
    try:
        user.save()
        return json.dumps(user.serialize()),200
    except Exception as e:
        traceback.print_exc()

        return str(e),500



@app.route('/user/<int:id>', methods=["DELETE"])
def delete_user(id):
    '''
    delete user by id.
    callers: all users
    '''
    user = User.query.filter(User.id == id).first()
    if user:
        user.delete()
        return "",204
    else:
        return "",404


@app.route('/constituencies', methods=["GET"])
def list_constituencies():
    '''
    list available constituencies
    callers: all users
    '''
    constituencies = Constituency.query.all()

    if constituencies:
        constituency_list = [constituency.serialize() for constituency in constituencies]

        return json.dumps(constituency_list)
    else:
        return "",404


@app.route('/')
def hello():
    return 'User Service is active'


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]


if __name__ =="__main__":
    app.run(debug=True,port=5000)
