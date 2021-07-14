import json

from app import app

from flask import request, abort, render_template
from sqlalchemy.exc import SQLAlchemyError

from app.database.database import Signals5m, Signals15m, Signals30m, Signals1h, db, DepositInfo, StatisticsInformation, \
    CurrentPosition, LastPosition, ClosedPosition, EnterSignal
import app.logic.statistics as statistics

"""
testing route
"""
# Main Root Page
@app.route('/test', methods=['GET'])
@app.route('/test/', methods=['GET'])
def test():
    #statistics.empty_all_tables()
    return '<h1>Test</h1>'


"""
Site pages
"""
# Main Root Page
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/signals/statistics/clear', methods=['GET'])
@app.route('/signals/statistics/clear/', methods=['GET'])
def statistics_clear_tables():
    statistics.empty_all_tables()
    return '<h1>Cleared</h1>'

@app.route('/signals/statistics/create_tables', methods=['GET'])
@app.route('/signals/statistics/create_tables/', methods=['GET'])
def statistics_create_table():
    statistics.create_all_tables()
    return '<h1>Done</h1>'

# Signals Statistic page
@app.route('/signals/statistics', methods=['GET'])
@app.route('/signals/statistics/', methods=['GET'])
def index_signals_statistics():
    return render_template('signals_statistic.html',
                           signals5m=Signals5m.query.order_by(Signals5m.date.desc()).all(),
                           signals1h=Signals1h.query.order_by(Signals1h.date.desc()).all(),
                           deposit_info=DepositInfo.query.first(),
                           statistics_info=StatisticsInformation.query.first(),
                           current_position=CurrentPosition.query.first(),
                           last_position=LastPosition.query.first(),
                           enter_signal=EnterSignal.query.first(),
                           closed_position_list=ClosedPosition.query.order_by(ClosedPosition.date.desc()).all())


# Analytics page
@app.route('/signals/analytics', methods=['GET'])
@app.route('/signals/analytics/', methods=['GET'])
def index_signals_analitycs():
    return render_template('signals_analitycs.html',
                           signal5m=Signals5m.query.order_by(Signals5m.date.desc()).first(),
                           signal15m=Signals15m.query.order_by(Signals15m.date.desc()).first(),
                           signal30m=Signals30m.query.order_by(Signals30m.date.desc()).first(),
                           signal1h=Signals1h.query.order_by(Signals1h.date.desc()).first())


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
            data = request.json
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
                statistics.analyse_trading_direction_by_signals_and_make_an_order()
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