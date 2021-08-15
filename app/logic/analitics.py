from os import abort

from sqlalchemy.exc import SQLAlchemyError

from app.database.database import db, Signals5m, Signals15m, Signals30m, Signals1h, \
    Analitics5m, Analitics15m, Analitics30m, Analitics1h, Balance_Signal


def commit_signal_to_database(data):
    if data['type'] == 'balance':
        try:
            balance = Balance_Signal.query.first()
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
    else:
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

def make_decision_5m():
    pass