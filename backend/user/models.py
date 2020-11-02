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


class User(db.Model): 
    # table names are autoamtically identified by converting class name to snakecase
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(13),unique=True)
    constituency_id = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    
    def serialize(self):
        serialized = {
            'id' : self.id,
            'name' : self.name,
            'phone' : self.phone,
            'constituency_id' : self.constituency_id,
            'created' : str(self.created)
        }
        return serialized

    def deserialize(self, json):
        #self.id  = json.get('id', None)
        self.name = json.get('name', self.name)
        self.phone = json.get('phone',self.phone)
        self.constituency_id = json.get('constituency_id',self.constituency_id)
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
    


class Constituency(db.Model): 
    # table names are autoamtically identified by converting class name to snakecase
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)    
    
    def serialize(self):
        serialized = {
            'id' : self.id,
            'name' : self.name,
        }
        return serialized

    def deserialize(self, json):
        #self.id  = json.get('id', None)
        self.name = json.get('name', self.name)
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
    
    
    
