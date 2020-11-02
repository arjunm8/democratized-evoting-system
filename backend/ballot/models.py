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


class Ballot(db.Model): 
    # table names are autoamtically identified by converting class name to snakecase
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    candidate_id = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    transaction_id = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    
    def serialize(self):
        serialized = {
            'id' : self.id,
            'user_id' : self.user_id,
            'candidate_id' : self.candidate_id,
            'image_url' : self.image_url,
            'transaction_id' : self.transaction_id,
            'created' : str(self.created)
        }
        return serialized

    def deserialize(self, json):
        #self.id  = json.get('id', None)
        self.user_id = json.get('user_id',self.user_id)
        self.candidate_id = json.get('candidate_id',self.candidate_id)
        self.image_url = json.get('image_url',self.image_url)
        self.transaction_id = json.get('transaction_id',self.transaction_id)
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
    


class Candidate(db.Model): 
    # table names are autoamtically identified by converting class name to snakecase
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    constituency_id = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    
    def serialize(self):
        serialized = {
            'id' : self.id,
            'name' : self.user_id,
            'image_url' : self.image_url,
            'constituency_id' : self.constituency_id,
            'created' : str(self.created)
        }
        return serialized

    def deserialize(self, json):
        #self.id  = json.get('id', None)
        self.name = json.get('name',self.name)
        self.image_url = json.get('image_url',self.image_url)
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
    
    
