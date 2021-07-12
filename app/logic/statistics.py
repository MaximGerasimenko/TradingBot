from app.database.database import db, Signals5m, Signals1h, \
    DepositInfo, StatisticsInformation, CurrentPosition, LastPosition, ClosedPosition, EnterSignal


class Decision:
    price = 0
    data = ''
    direction = ''
    balance = ''
    decision = ''

def create_all_tables():
    if DepositInfo.query.first() is None:
        db.session.add(DepositInfo(deposit_start=50.0, deposit_current=50.0, trading_multiple=10, profit=0.0, profit_percentage=0.0))
        db.session.commit()
    if StatisticsInformation.query.first() is None:
        db.session.add(StatisticsInformation(count_trades=0, count_profit_trades=0, count_lost_trades=0, percent_profit_trades=0.0))
        db.session.commit()
    if CurrentPosition.query.first() is None:
        db.session.add(CurrentPosition(direction='none', deposit=0.0, deposit_with_multiple=0.0, amount=0.0, enter_price=0.0))
        db.session.commit()
    if LastPosition.query.first() is None:
        db.session.add(LastPosition(direction='none', deposit=0.0, profit=0.0, earnings=0.0, earnings_percentage=0.0, enter_price=0.0, exit_price=0.0))
        db.session.commit()
    if EnterSignal.query.first() is None:
        db.session.add(EnterSignal(type='RSI', signal='long', price=0.0, price_hight=0.0, price_low=0.0, balance=0.0))
        db.session.commit()

def analyse_1h_signal():

    try:
        last_signal = Signals1h.query.order_by(Signals1h.date.desc()).first()
    except:
        print('ERROR::analyse_1h_signal : Cant load 1 hour signal')
    decision_1h = Decision()

    if last_signal.price >= last_signal.balance:
        decision_1h.balance = 'long'
    elif last_signal.prive < last_signal.balance:
        decision_1h.balance = 'short'

    if last_signal.signal == 'long':
        decision_1h.direction = 'long'
    elif last_signal.signal == 'short':
        decision_1h.direction = 'short'

    if decision_1h.direction == 'long' and decision_1h.balance == 'long':
        decision_1h.decision = 'long'
    elif decision_1h.direction == 'short' and decision_1h.balance == 'short':
        decision_1h.decision = 'short'
    else:
        decision_1h.decision = 'ignore'

    return decision_1h

def analyse_5m_signal():
    try:
        last_signal = Signals5m.query.order_by(Signals5m.date.desc()).first()
        decision_5m = Decision()

        decision_5m.data=last_signal
        decision_5m.price = last_signal.price
    except:
        print('ERROR::analyse_5m_signal : Cant load 5m signal')

    if last_signal.price >= last_signal.balance:
        decision_5m.balance = 'long'
    elif last_signal.prive < last_signal.balance:
        decision_5m.balance = 'short'

    if last_signal.signal == 'long':
        decision_5m.direction = 'long'
    elif last_signal.signal == 'short':
        decision_5m.direction = 'short'

    if decision_5m.direction == 'long' and decision_5m.balance == 'long':
        decision_5m.decision = 'long'
    elif decision_5m.direction == 'short' and decision_5m.balance == 'short':
        decision_5m.decision = 'short'
    else:
        decision_5m.decision = 'ignore'

    return decision_5m


def open_position(dec_5m):
    deposit_info = DepositInfo.query.first()
    statistics_info = StatisticsInformation.query.first()
    current_position = CurrentPosition.query.first()

    # creating position
    current_position.direction = dec_5m.decision
    current_position.deposit = deposit_info.deposit_current / 10
    current_position.deposit_with_multiple = current_position.deposit * deposit_info.trading_multiple
    current_position.amount = current_position.deposit_with_multiple / dec_5m.price
    current_position.enter_price = dec_5m.price
    db.session.commit()

    # changing deposit data
    deposit_info.deposit_current -= current_position.deposit
    db.session.commit()

    # changing statistics data
    statistics_info.count_trades += 1
    db.session.commit()

    # Changing enter signal
    enter_signal = EnterSignal.query.first()
    enter_signal.type = dec_5m.data.type
    enter_signal.signal = dec_5m.data.signal
    enter_signal.balance = dec_5m.data.balance
    enter_signal.price = dec_5m.data.price
    enter_signal.price_hight = dec_5m.data.price_hight
    enter_signal.price_low = dec_5m.data.price_low


def close_current_position(dec_5m):
    deposit_info = DepositInfo.query.first()
    statistics_info = StatisticsInformation.query.first()
    current_position = CurrentPosition.query.first()
    last_position = LastPosition.query.first()

    # Changing last position on that position
    last_position.direction = current_position.direction
    last_position.deposit = current_position.deposit
    last_position.profit = (current_position.amount * dec_5m.price) / deposit_info.trading_multiple
    last_position.earnings = last_position.profit - last_position.deposit
    last_position.earnings_percentage = (last_position.earnings / last_position.deposit) * 100
    last_position.enter_price = current_position.enter_price
    last_position.exit_price = dec_5m.price
    db.session.commit()

    last_position = LastPosition.query.first()

    # Adding Last Position to the list
    db.session.add(ClosedPosition(direction=last_position.direction, deposit=last_position.deposit, earnings=last_position.earnings, earnings_percentage=last_position.earnings_percentage, enter_price=last_position.enter_price, exit_price=last_position.exit_price))
    db.session.commit()

    # Changing current position status
    current_position.direction = 'none'
    current_position.deposit = 0.0
    current_position.deposit_with_multiple = 0.0
    current_position.amount = 0.0
    current_position.enter_price = 0.0
    db.session.commit()

    # Changina deposit info
    deposit_info.deposit_current += last_position.profit
    deposit_info.profit += last_position.earnings
    deposit_info.profit_percentage = (deposit_info.profit / deposit_info.deposit_start) * 100
    db.session.commit()

    # Changing statistics data
    if last_position.earnings > 0:
        statistics_info.count_profit_trades += 1
    else:
        statistics_info.count_lost_trades += 1
    statistics_info.percent_profit_trades = (statistics_info.count_profit_trades / statistics_info.count_trades) * 100
    db.session.commit()


def analyse_trading_direction_by_signals_and_make_an_order():
    current_position = CurrentPosition.query.first()
    dec_5m = analyse_5m_signal()
    dec_1h = analyse_1h_signal()

    # Deciding about position
    # If have a position and want to close
    if current_position.direction == 'long' and dec_5m.direction == 'short' and dec_1h.direction == 'long':
        close_current_position(dec_5m)
    elif current_position.direction == 'short' and dec_5m.direction == 'long' and dec_1h.direction == 'short':
        close_current_position(dec_5m)
    elif current_position.direction == 'long' and dec_5m.direction == 'short' and dec_1h.direction == 'short':
        close_current_position(dec_5m)
    elif current_position.direction == 'short' and dec_5m.direction == 'long' and dec_1h.direction == 'long':
        close_current_position(dec_5m)
    # If have not a position and want to open
    elif current_position.direction == 'none' and dec_5m.decision == 'long' and dec_1h.direction == 'long':
        open_position(dec_5m)
    elif current_position.direction == 'none' and dec_5m.decision == 'short' and dec_1h.direction == 'short':
        open_position(dec_5m)
    # When ignoring signal
    # Have no a position
    elif current_position.direction == 'none' and dec_5m.decision == 'long' and dec_1h.direction == 'short':
        return
    elif current_position.direction == 'none' and dec_5m.decision == 'short' and dec_1h.direction == 'long':
        return
    # Have a position
    elif current_position.direction == 'long' and dec_5m.direction == 'long' and dec_1h.direction == 'long':
        return
    elif current_position.direction == 'short' and dec_5m.direction == 'short' and dec_1h.direction == 'short':
        return
    # Error
    else:
        print('ERROR:: CANT DECIDE ABOUT POSITION NEED TO UPDATE: current_position.direction: ' + current_position.direction
              + ', 5m_dir: ' + dec_5m.direction + ', 5m_decision: ' + dec_5m.decision + ', 1h_dir: ' + dec_1h.direction)

    if dec_1h.direction == dec_5m.decision:
        open_position(dec_5m)
    else:
        print('ignore')