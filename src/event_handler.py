import logging

def event_parser(new_binance_event) -> dict:
    '''Parses the raw event
    
    Returns: Dict of Parsed Event or None
    '''
    event_type = new_binance_event['e']

    if event_type == "ALGO_UPDATE": # Algo Orders - for SL
        return _parse_SL_order(new_binance_event)
    elif event_type == "ORDER_TRADE_UPDATE": # Regular Orders - for MO
        if new_binance_event['o'].get('st') and new_binance_event['o']['st'] == "ALGO_CONDITION": 
            logging.info("Ignoring the duplicate ORDER_TRADE_UPDATE event sent for Algo SL orders")
            return None
        return _parse_MO_order(new_binance_event)
    else:
        logging.info(f"Ignoring events of type {event_type}")
        return None


def _parse_SL_order(new_binance_event) -> dict:
    'Used for parsing SL events emitted from algoOrder API - see samples/websockets/stoploss_orders.json' 
    assert new_binance_event['e'] == "ALGO_UPDATE"
    
    try:
        parsed_event = {
            "order_id": new_binance_event["o"]["aid"], # this is different from normal orders
            "status": new_binance_event["o"]["X"], # NEW / EXPIRED / FINISHED / CANCELED
            "symbol": new_binance_event["o"]["s"],
            "side": new_binance_event["o"]["S"], # BUY/SELL
            "type": new_binance_event["o"]["o"], # this is different from normal orders; will be STOP_MARKET 
            "qty": new_binance_event["o"]["q"],
        }

        #NEED TO IGNORE TRIGGERING AND TRIGGERED
        if parsed_event['type'] != "STOP_MARKET":
            raise ValueError("Only STOP_MARKET Orders should be parsed in this function")
        
        if parsed_event['status'] == ("TRIGGERING" or "TRIGGERED"):
            logging.info(f"Ignoring SL events of status {parsed_event['status']}")
            return None

        parsed_event['direction'] = "LONG" if parsed_event['side'] == "SELL" else "SHORT"

        if parsed_event['status'] == "NEW":
            parsed_event['created_at'] = new_binance_event["T"]
            parsed_event['ask_price'] = new_binance_event["o"]["tp"]

        elif parsed_event['status'] == "FINISHED":
            parsed_event['status'] = "FILLED" #changing this to standardize with the rest
            parsed_event['filled_price'] = new_binance_event["o"]["ap"] 
            parsed_event['updated_at'] = new_binance_event["T"]

        elif parsed_event['status'] == "CANCELED":
            parsed_event['updated_at'] = new_binance_event["T"]

        logging.info(f"Successfully parsed event, returning: {parsed_event}")
        return parsed_event
    except Exception as e:
        logging.info(f"An exception occurred when parsing event: {e}")
        raise

def _parse_MO_order(new_binance_event) -> dict:
    'Used for parsing MO events order API - see samples/websockets/enter_market_order.json' 
    assert new_binance_event['e'] == "ORDER_TRADE_UPDATE"
    
    try:
        parsed_event = {
            "order_id": new_binance_event["o"]["i"],
            "status": new_binance_event["o"]["X"], # NEW / EXPIRED / FILLED / CANCELED
            "symbol": new_binance_event["o"]["s"],
            "side": new_binance_event["o"]["S"], # BUY/SELL
            "type": new_binance_event["o"]["ot"], # MARKET / TAKE_PROFIT / STOP_MARKET / LIMIT
            "qty": new_binance_event["o"]["q"],
        }
        if parsed_event['type'] != "MARKET":
            raise ValueError("Only Market Orders should be parsed in this function")

        parsed_event['direction'] = "LONG" if parsed_event['side'] == "BUY" else "SHORT"
        
        if parsed_event['status'] == "NEW":
            parsed_event['created_at'] = new_binance_event["T"]
        
        if parsed_event['status'] == "FILLED":
            parsed_event['ask_price'] = parsed_event['filled_price'] = new_binance_event["o"]["ap"]
        
        if parsed_event['status'] == "FILLED" or parsed_event['status'] == "CANCELED":
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