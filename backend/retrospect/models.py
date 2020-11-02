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


class Retrospect(db.Model): 
    # table names are autoamtically identified by converting class name to snakecase
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(255))
    ballot_id = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    
    def serialize(self):
        serialized = {
            'id' : self.id,
            'image_url' : self.image_url,
            'ballot_id' : self.ballot_id,
            'created' : str(self.created)
        }
        return serialized

    def deserialize(self, json):
        #self.id  = json.get('id', None)
        self.image_url = json.get('image_url',self.image_url)
        self.ballot_id = json.get('ballot_id',self.ballot_id)
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
    
    
    
