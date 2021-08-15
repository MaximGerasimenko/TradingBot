class last_position:
    deposit = 0.0
    earnings = 0.0
    profit = 0.0
    earnings_percentage = 0.0

trading_multiple = 10
last_position.enter_price = 35000
last_position.exit_price = 34000
last_position.deposit = 5.0

last_position.earnings = ((last_position.deposit / last_position.enter_price)
                          * (last_position.enter_price - last_position.exit_price)) * trading_multiple
last_position.profit = last_position.deposit + last_position.earnings
last_position.earnings_percentage = (last_position.earnings / last_position.deposit) * 100


print(last_position.deposit)
print(last_position.earnings)
print(last_position.profit)
print(last_position.earnings_percentage)
print(last_position.enter_price)
print(last_position.exit_price)