from flask import Flask, request, abort, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import json

app = Flask(__name__)

"""
Database settings
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


"""
Site pages
"""
# Main Root Page
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    return render_template('index.html')


# Signals Statistic page
@app.route('/signals/stat', methods=['GET'])
@app.route('/signals/stat/', methods=['GET'])
def index_signals_statistics():
    return render_template('signals_statistic.html',
                           signals5m=Signals5m.query.order_by(TestSignal.date.desc()).all(),
                           signals15m=Signals15m.query.order_by(TestSignal.date.desc()).all(),
                           signals30m=Signals30m.query.order_by(TestSignal.date.desc()).all(),
                           signals1h=Signals1h.query.order_by(TestSignal.date.desc()).all())
# 5m Signals Page
@app.route('/signals/5m', methods=['GET'])
@app.route('/signals/5m/', methods=['GET'])
def index_signals_5m():
    return render_template('signals_5m.html',
                           signals=Signals5m.query.order_by(Signals5m.date.desc()).all(),
                           last_signal=Signals5m.query.order_by(Signals5m.date.desc()).first())
# 15m Signals Page
@app.route('/signals/15m', methods=['GET'])
@app.route('/signals/15m/', methods=['GET'])
def index_signals_15m():
    return render_template('signals_15m.html',
                           signals=Signals15m.query.order_by(Signals15m.date.desc()).all(),
                           last_signal=Signals15m.query.order_by(Signals15m.date.desc()).first())
# 30m Signals Page
@app.route('/signals/30m', methods=['GET'])
@app.route('/signals/30m/', methods=['GET'])
def index_signals_30m():
    return render_template('signals_30m.html',
                           signals=Signals30m.query.order_by(Signals30m.date.desc()).all(),
                           last_signal=Signals30m.query.order_by(Signals30m.date.desc()).first())
# 1h Signals Page
@app.route('/signals/1h', methods=['GET'])
@app.route('/signals/1h/', methods=['GET'])
def index_signals_1h():
    return render_template('signals_1h.html',
                           signals=Signals1h.query.order_by(Signals1h.date.desc()).all(),
                           last_signal=Signals1h.query.order_by(Signals1h.date.desc()).first())


# API Root page
@app.route('/api', methods=['GET'])
@app.route('/api/', methods=['GET'])
def index_api():
    return render_template('api_page.html')


# Binance API page
@app.route('/api/binance', methods=['GET'])
@app.route('/api/binance/', methods=['GET'])
def index_api_binance():
    return render_template('api_binance.html')


# Webhooks Root Page
@app.route('/api/webhook', methods=['GET'])
@app.route('/api/webhook/', methods=['GET'])
def index_api_webhook():
    return 'WebhookAPI'


# Main Webhook for TradingView signals
@app.route('/webhook', methods=['POST'])
@app.route('/webhook/', methods=['POST'])
def webhook():
    global data
    if request.method == 'POST':
        try:
            data = json.load(request.json)
        except:
            print('Cant load JSON data')
        if data['timeframe'] == '5m':
            try:
                db.session.add(Signals5m(type=data['type'], signal=data['signal'],
                                         price=data['price'], price_hight=data['hight'], price_low=data['low'],
                                         balance=data['balance']))
                db.session.commit()
                return 'success', 200
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                print('Error while adding 5m signal.')
                print(error)
                return abort(400)
        elif data['timeframe'] == '15m':
            try:
                db.session.add(Signals15m(type=data['type'], signal=data['signal'],
                                          price=data['price'], price_hight=data['hight'], price_low=data['low'],
                                          balance=data['balance']))
                db.session.commit()
                return 'success', 200
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                print('Error while adding 15m signal.')
                print(error)
                return abort(400)
        elif data['timeframe'] == '30m':
            try:
                db.session.add(Signals30m(type=data['type'], signal=data['signal'],
                                          price=data['price'], price_hight=data['hight'], price_low=data['low'],
                                          balance=data['balance']))
                db.session.commit()
                return 'success', 200
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                print('Error while adding 30m signal.')
                print(error)
                return abort(400)
        elif data['timeframe'] == '1h':
            try:
                db.session.add(Signals1h(type=data['type'], signal=data['signal'],
                                         price=data['price'], price_hight=data['hight'], price_low=data['low'],
                                         balance=data['balance']))
                db.session.commit()
                return 'success', 200
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                print('Error while adding 1h signal.')
                print(error)
                return abort(400)


"""
Starting Application
Change debug=False before deploy
"""
if __name__ == '__main__':
    app.run(debug=True)
