import random

def trade_simulator():
    trade_amount = random.randint(-100, 100)
    currency_pair = random.choice(["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF"])
    entry_price = random.random() * 1
    formatted_entry_price = '{:.2f}'.format(entry_price)
    exit_price = random.random() * 1
    formatted_exit_price = '{:.2f}'.format(exit_price)
    trade_type = random.choice(["long", "short"])
    return trade_amount, currency_pair, formatted_entry_price, formatted_exit_price, trade_type