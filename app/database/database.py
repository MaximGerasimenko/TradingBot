from app import app
from app import db

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Testing signals DB
class TestSignal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<TestSignal %r>' % self.id


# Signals for 5m
class Signals5m(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(10), nullable=False)
    signal = db.Column(db.String(5), nullable=False)
    price = db.Column(db.Float, nullable=False)
    price_hight = db.Column(db.Float, nullable=False)
    price_low = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<TestSignal %r>' % self.id


# Signals for 15m
class Signals15m(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(10), nullable=False)
    signal = db.Column(db.String(5), nullable=False)
    price = db.Column(db.Float, nullable=False)
    price_hight = db.Column(db.Float, nullable=False)
    price_low = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<TestSignal %r>' % self.id


# Signals for 30m
class Signals30m(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(10), nullable=False)
    signal = db.Column(db.String(5), nullable=False)
    price = db.Column(db.Float, nullable=False)
    price_hight = db.Column(db.Float, nullable=False)
    price_low = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<TestSignal %r>' % self.id


# Signals for 1h
class Signals1h(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(10), nullable=False)
    signal = db.Column(db.String(5), nullable=False)
    price = db.Column(db.Float, nullable=False)
    price_hight = db.Column(db.Float, nullable=False)
    price_low = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<TestSignal %r>' % self.id

