import logging
def event_parser(new_binance_event) -> dict:
    try:
        parsed_event = {
            "order_id": new_binance_event["o"]["i"],
            "group_id": new_binance_event["o"]["c"],
            "status": new_binance_event["o"]["X"], # NEW / EXPIRED / FILLED / CANCELED
            "symbol": new_binance_event["o"]["s"],
            "side": new_binance_event["o"]["S"], # BUY/SELL
            "type": new_binance_event["o"]["ot"], # MARKET / TAKE_PROFIT / STOP_MARKET
            "qty": new_binance_event["o"]["q"],
        }
        if parsed_event['type'] == "MARKET":
            parsed_event['direction'] = "LONG" if parsed_event['side'] == "BUY" else "SHORT"
        elif type == "TAKE_PROFIT":
            parsed_event['direction'] = "LONG" if parsed_event['side'] == "SELL" else "SHORT"
        elif type == "STOP_MARKET":
            parsed_event['direction'] = "LONG" if parsed_event['side'] == "SELL" else "SHORT"
        
        if parsed_event['status'] == "NEW":
            parsed_event['created_at'] = new_binance_event["T"]
        
        if parsed_event['type'] == "MARKET" and parsed_event['status'] == "FILLED":
            parsed_event['ask_price'] = parsed_event['filled_price'] = new_binance_event["o"]["ap"]
        
        if parsed_event['type'] != "MARKET" and parsed_event['status'] == "FILLED":
            parsed_event['filled_price'] = new_binance_event["o"]["ap"]
        elif parsed_event['type'] != "MARKET" and parsed_event['status'] == "NEW":
            parsed_event['ask_price'] = new_binance_event["o"]["sp"]
        
        if parsed_event['status'] == "FILLED":
            parsed_event['updated_at'] = new_binance_event["T"]
        
        logging.info(f"Successfully parsed event, returning: {parsed_event}")
        return parsed_event
    except Exception as e:
        logging.info(f"An exception occurred when parsing event: {e}")
        raise

# def is_new_market_order(new_binance_event):
'''
CREATE TABLE orders (
	order_id BIGINT,
	group_id BIGINT,
	symbol VARCHAR(16),
	order_type VARCHAR(24),
	ask_price DECIMAL,
	filled_price DECIMAL,
	side VARCHAR(4),
	created_at TIMESTAMP
);
'''


'''
{
    "e": "ORDER_TRADE_UPDATE",
    "T": 1749013292798,
    "E": 1749013292798,
    "o": {
        "s": "SOLUSDT",
        "c": "fOPYqvypuFM2LKJ3ihzKFZ",
        "S": "BUY",
        "o": "MARKET",
        "f": "GTC",
        "q": "0.09",
        "p": "0",
        "ap": "0",
        "sp": "0",
        "x": "NEW",
        "X": "NEW",
        "i": 121058809222,
        "l": "0",
        "z": "0",
        "L": "0",
        "n": "0",
        "N": "USDT",
        "T": 1749013292798,
        "t": 0,
        "b": "0",
        "a": "0",
        "m": False,
        "R": False,
        "wt": "CONTRACT_PRICE",
        "ot": "MARKET",
        "ps": "BOTH",
        "cp": False,
        "rp": "0",
        "pP": False,
        "si": 0,
        "ss": 0,
        "V": "EXPIRE_MAKER",
        "pm": "NONE",
        "gtd": 0
    }
}
'''