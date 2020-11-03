#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 2 11:06:59 2020

@author: arjun
"""

# apps.members.models
from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()


class Candidate(db.Model):
    # table names are autoamtically identified by converting class name to snakecase
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    constituency_id = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def get_str_id(self):
        return str(self.id)

    def serialize(self):
        serialized = {
            'id' : self.id,
            'name' : self.name,
            'image_url' : self.image_url,
            'constituency_id' : self.constituency_id,
            'created' : str(self.created)
        }
        return serialized

    def save(self, commit=True):
            db.session.add(self)
            if(commit):
                db.session.commit()
            return self


    def delete(self, commit=True):
        db.session.delete(self)
        if(commit):
            db.session.commit()
        return self
