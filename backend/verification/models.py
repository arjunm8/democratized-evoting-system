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


class Document(db.Model): 
    # table names are autoamtically identified by converting class name to snakecase
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255))
    kind = db.Column(db.String(32))
    number = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def serialize(self):
        serialized = {
            'id' : self.id,
            'user_id' : self.user_id,
            'kind' : self.kind,
            'number' : self.number,
            'image_url' : self.image_url,
            'created' : str(self.created)
        }
        return serialized

    def deserialize(self, json):
        #self.id  = json.get('id', None)
        self.user_id = json.get('user_id', self.user_id)
        self.kind = json.get('kind',self.kind)
        self.number = json.get('number',self.kind)
        self.image_url = json.get('image_url',self.image_url)
        return self
    

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
