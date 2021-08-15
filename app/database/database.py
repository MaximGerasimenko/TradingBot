from app import app
from app import db

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


"""
Analytics models
"""
# Main information about deposit
class DepositInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deposit_start = db.Column(db.Float, nullable=False, default=50.0)
    deposit_current = db.Column(db.Float, default=deposit_start)
    trading_multiple = db.Column(db.Integer, default=10)
    profit = db.Column(db.Float, default=0.0)
    profit_percentage = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return '<DepositInfo %r>' % self.id

# Main Statistics information
class StatisticsInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    count_trades = db.Column(db.Integer, default=0)
    count_profit_trades = db.Column(db.Integer, default=0)
    count_lost_trades = db.Column(db.Integer, default=0)
    percent_profit_trades = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return '<StatisticsInformation %r>' % self.id

# Current Position
class CurrentPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    direction = db.Column(db.String(10), nullable=False, default='none')
    deposit = db.Column(db.Float, default=0.0)
    deposit_with_multiple = db.Column(db.Float, default=0.0)
    amount = db.Column(db.Float, default=0.0)
    enter_price = db.Column(db.Float, default=0.0)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<CurrentPosition %r>' % self.id

# Last Position
class LastPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    direction = db.Column(db.String(10), nullable=False, default='last pos')
    deposit = db.Column(db.Float, default=0.0)
    profit = db.Column(db.Float, default=0.0)
    earnings = db.Column(db.Float, default=0.0)
    earnings_percentage = db.Column(db.Float, default=0.0)
    enter_price = db.Column(db.Float, default=0.0)
    exit_price = db.Column(db.Float, default=0.0)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<LastPosition %r>' % self.id


# Closed Position List
class ClosedPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    direction = db.Column(db.String(10), nullable=False, default='last pos')
    deposit = db.Column(db.Float, default=0.0)
    earnings = db.Column(db.Float, default=0.0)
    earnings_percentage = db.Column(db.Float, default=0.0)
    enter_price = db.Column(db.Float, default=0.0)
    exit_price = db.Column(db.Float, default=0.0)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<ClosedPosition %r>' % self.id


# Signals for 5m
class EnterSignal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(10), nullable=False)
    signal = db.Column(db.String(5), nullable=False)
    price = db.Column(db.Float, nullable=False)
    price_hight = db.Column(db.Float, nullable=False)
    price_low = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<EnterSignal %r>' % self.id

# Testing signals DB
class TestSignal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<TestSignal %r>' % self.id


# Signals for 5m
class Balance_Signal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    balance = db.Column(db.Float, nullable=True)
    price = db.Column(db.Float, nullable=True)
    price_hight = db.Column(db.Float, nullable=True)
    price_low = db.Column(db.Float, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Balance_Signal %r>' % self.id


# Signals for 5m
class Signals5m(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(10), nullable=True)
    signal = db.Column(db.String(5), nullable=True)
    rop = db.column(db.Float, nullable=True)
    price = db.Column(db.Float, nullable=True)
    price_hight = db.Column(db.Float, nullable=True)
    price_low = db.Column(db.Float, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Signals5m %r>' % self.id


# Signals for 15m
class Signals15m(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(10), nullable=True)
    signal = db.Column(db.String(5), nullable=True)
    rop = db.column(db.Float, nullable=True)
    price = db.Column(db.Float, nullable=True)
    price_hight = db.Column(db.Float, nullable=True)
    price_low = db.Column(db.Float, nullable=True)
    balance = db.Column(db.Float, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Signals15m %r>' % self.id


# Signals for 30m
class Signals30m(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(10), nullable=True)
    signal = db.Column(db.String(5), nullable=True)
    rop = db.column(db.Float, nullable=True)
    price = db.Column(db.Float, nullable=True)
    price_hight = db.Column(db.Float, nullable=True)
    price_low = db.Column(db.Float, nullable=True)
    balance = db.Column(db.Float, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Signals30m %r>' % self.id


# Signals for 1h
class Signals1h(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(10), nullable=True)
    signal = db.Column(db.String(5), nullable=True)
    rop = db.column(db.Float, nullable=True)
    price = db.Column(db.Float, nullable=True)
    price_hight = db.Column(db.Float, nullable=True)
    price_low = db.Column(db.Float, nullable=True)
    balance = db.Column(db.Float, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Signals1h %r>' % self.id


# Analitics 5m
class Analitics5m(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    decision = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return '<Analitics5m %r>' % self.decision


# Analitics 15m
class Analitics15m(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    decision = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return '<Analitics15m %r>' % self.decision


# Analitics 30m
class Analitics30m(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    decision = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return '<Analitics30m %r>' % self.decision


# Analitics 1h
class Analitics1h(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    decision = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return '<Analitics1h %r>' % self.decision