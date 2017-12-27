import sys
sys.path.append("../")

# must include the below when running data/dexcomG5.py, comment out otherwise
# from flask import Flask, jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
# app = Flask(__name__)
# db = SQLAlchemy(app)

# must comment out the below when running data/dexcomG5.py
from app import *

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    username = db.Column(db.String(128), unique=True)

    def __init__(self, name, username):
        self.username = username
        self.name = name

    def __repr__(self):
        return '<USER {}>'.format(self.name)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(75))
    manufacturerID = db.Column(db.String(20), unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User',
        backref=db.backref('devices', lazy='dynamic'))

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meas_date = db.Column(db.DateTime)
    event_type = db.Column(db.String(20))
    manufacturerID = db.Column(db.String(20))
    gluc_value = db.Column(db.Integer)
    insulin_value = db.Column(db.Integer)
    carb = db.Column(db.Float)
    #joins are worse than duplicated data

    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship('Device')
        # backref=db.backref('devices', lazy='dynamic'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
        # backref=db.backref('users', lazy='dynamic'))
