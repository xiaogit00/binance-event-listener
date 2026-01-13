import json 

def calculateTrailingValue(candle_data, direction, actual_entry_price):

    if direction == "LONG":
        last_low = float(json.loads(candle_data['candle_data'])['low'])
        trailing_percentage = float(json.loads(candle_data['trade_metadata'])['trailing_percentage'])
        trailing_value = (actual_entry_price - last_low) * trailing_percentage
        trailing_price = actual_entry_price + trailing_value
        next_stoploss_price = last_low + trailing_value 
        return last_low, trailing_value, trailing_price, next_stoploss_price
    else:
        last_high = float(json.loads(candle_data['candle_data'])['high'])
        trailing_percentage = float(json.loads(candle_data['trade_metadata'])['trailing_percentage'])
        trailing_value = (last_high - actual_entry_price) * trailing_percentage
        trailing_price = actual_entry_price - trailing_value
        next_stoploss_price = last_high - trailing_value  
        return last_high, trailing_value, trailing_price, next_stoploss_price


'''
candle_data
{'order_id': 188999740044, 'candle_data': '{"open": "139.10", "high": "149.10", "low": "129.10", "close": "138.10"}', 'trade_metadata': '{"risk_amount": 10, "fee": 0.1, "portfolio_threshold": 20, "rv_period": 2, "ema_period": 9, "rv_threshold": 2.8, "trailing_percentage": 0.7}', 'created_at': '2026-01-13T10:49:06.448679+00:00'}
'''